import csv
import re
import sys


NONALPHA_REX = re.compile('[^\d^\w]')
MEDIAN_REX = re.compile(' median: ([\-?\d\.]+)')
CATEGORY_REX = re.compile('\[(\(.+)\]$')
ITEM_REX = re.compile("\(\'(.*?)\', \d+\)")
KILL_X = re.compile(r"\\x\w\d")


def safe_key(key, value):
    if not value:
        value = 'emptycat'
    return '%s_%s' % (key, NONALPHA_REX.sub('', KILL_X.sub('', value)))


def read_rule(row):
    key = row.split(',')[0].strip()
    m = MEDIAN_REX.findall(row)
    if m:
        if 'empty: ' not in row:
            print key, 'no empties'
            return key, 'keep', []
        return key, 'num', m[0]

    try:
        cat = CATEGORY_REX.findall(row)[0]
    except IndexError:
        print row
        raise IndexError
    cats = ITEM_REX.findall(cat)
    if len(cats) == 10:
        cats += ['N/Arest']
        print 'WARNING: Cannot split %s to more than 10 columns. Adding N/A.' % key, cats
    if len(cats) == 2:
        return key, 'keep', []
    return key, 'cat', [c.decode('utf8').encode('latin1') for c in cats]


def read_column(name):
    imputes = {}
    splits = {}
    keep = []

    with open(name) as f:
        f.readline()
        for row in f:
            row = row.strip()
            if not row:
                continue
            if not row.startswith('+'):
                continue
            row = row[1:].strip()
            column_name, typ, extra = read_rule(row)
            #  column_name = NONALPHA_REX.sub('', column_name)
            column_name = column_name.decode('utf8').encode('latin1')

            if typ == 'num':
                imputes[column_name] = extra
            elif typ == 'cat':
                splits[column_name] = extra
            elif typ == 'keep':
                keep.append(column_name)

    return imputes, splits, keep


def isimpute(s):
    return '%s_empty' % s


class FixCSV:

    def __init__(self, column_name, incsv_name, outcsv_name):
        self.imputes, self.splits, self.keeps = read_column(column_name)
        print 'Imputing', self.imputes
        print 'Splitting', self.splits
        print 'Keep', self.keeps

        self.transfer(incsv_name, outcsv_name)

    def expand_headers(self, headers):
        h2 = headers
        for t in self.splits:
            i = h2.index(t)
            h2 = h2[:i] + [safe_key(t, k) for k in self.splits[t]] + h2[i + 1:]
        for t in self.imputes:
            i = h2.index(t)
            h2 = h2[:i] + [isimpute(t)] + h2[i:]
        return h2

    def transfer(self, incsv_name, outcsv_name):
        with open(incsv_name) as inf:
            inc = csv.DictReader(inf)
            headers = inc.fieldnames
            missing = set(headers) - (set(self.imputes).union(self.splits).union(self.keeps))
            if missing:
                raise KeyError('Missing %s' % missing)
            new_headers = self.expand_headers(headers)
            print new_headers

            with open(outcsv_name, 'wt') as outf:
                outc = csv.DictWriter(outf, fieldnames=new_headers)
                outc.writeheader()
                for row in inc:
                    for key, val in self.imputes.iteritems():
                        if row[key]:
                            row[isimpute(key)] = '0'
                        else:
                            row[key] = val
                            row[isimpute(key)] = '1'

                    for key, targets in self.splits.iteritems():
                        for t in targets:
                            row[safe_key(key, t)] = '0'
                        if row[key] in targets:
                            rkey = row[key]
                        else:
                            rkey = 'N/Arest'
                        row[safe_key(key, rkey)] = '1'
                        del row[key]

                    for key in self.keeps:
                        try:
                            float(row[key])
                        except ValueError:
                            row[key] = '-1'

                    outc.writerow(row)

if __name__ == '__main__':
    FixCSV(*sys.argv[1:])
