# -*- coding: utf-8 -*-

"""
Usage:
python merge_csv.py 1.csv 2.csv 3.csv ..etc
"""
import csv
import sys
import itertools
import re

from datetime import datetime

DATE1_REX = re.compile('\d\d/\d\d/\d\d')
DATE2_REX = re.compile('\d\d\d\d-\d\d-\d\d')


def clean(x):
    """
    Volvofinans specific cleaning.
    Clean float to int.
    Clean their specific date formats to number of days ago.
    """
    if x.endswith('.0'):
        return x[:-2]

    d = None
    if DATE1_REX.match(x):
        d = datetime.strptime(x, '%d/%m/%y')
    elif DATE2_REX.match(x):
        d = datetime.strptime(x, '%Y-%m-%d')

    if d is not None:
        return str((datetime.now() - d).days)

    return x


class OrderedCSV:

    def __init__(self, fname):
        """
        Keyword Arguments:
        fname -- Input CSV
        """
        self.fname = fname
        self.finished = False
        self.doubles = False
        self.csv = csv.reader(open(fname))
        self.headers = self.csv.next()
        self.empty = [''] * (len(self.headers) - 1)

        self.get_cur()

    def get_cur(self):
        try:
            self.row = [clean(x) for x in self.csv.next()]
            self.cid = int(self.row[0])
        except StopIteration:
            self.cid = 1000000000000000
            self.row = self.empty
            self.finished = True
        return self.cid

    def __getitem__(self, key):
        if key == self.cid:
            row = self.row
            while self.get_cur() == key:
                if not self.doubles:
                    print self.fname.split('/')[-1], 'has double IDs'
                    self.doubles = True
            return row[1:]
        else:
            return self.empty

    def __lt__(self, other):
        return self.cid < other.cid


def merge(target, fnames):
    """
    Keyword Arguments:
    target -- Output CSV
    fnames -- Input CSVs. Columns will be ordered same as fnames.

    First column in each field is assumed to have an ID.
    """
    cs = [OrderedCSV(fname) for fname in fnames]
    with open(target, 'wt') as outf:
        outc = csv.writer(outf)
        totheaders = list(itertools.chain([cs[0].headers[0]], *[c.headers[1:] for c in cs]))
        print '%d columns' % len(totheaders)
        outc.writerow(totheaders)

        while True:
            cid = min(cs).cid
            maincid = cs[0].cid
            outrows = [c[cid] for c in cs]
            if maincid == cid:
                print cid
                outc.writerow(list(itertools.chain([str(cid)], *outrows)))
            else:
                print 'skipping', cid
            if all(c.finished for c in cs):
                break


if __name__ == '__main__':
    merge(sys.argv[1], sys.argv[2:])
