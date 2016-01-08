import csv
import re
import sys

import csv_fix
import smart_csv

ITEM_REX = re.compile("\(\'(.*?)\', (\d+)\)")


def find_outliers(txtfile, limit):
    with open(txtfile) as f:
        for i, row in enumerate(f):
            if i == 0:
                continue
            field = row.split(',')[0].strip()
            try:
                cat = csv_fix.CATEGORY_REX.findall(row)[0]
            except IndexError:
                continue

            cats = ITEM_REX.findall(cat)
            if len(cats) >= 10:
                continue
            for name, val in cats:
                if int(val) <= limit:
                    print field, i, name, val
                    yield i, name


def has_outliers(outliers, row):
    for i, name in outliers:
        if i >= len(row):
            print len(row), i, row
        if row[i].strip() == name:
            print i, name
            return True
    return False


def kill_outliers(incsv_name, outcsv_name, outliers):
    skipped = 0
    kept = 0
    with open(incsv_name) as inf:
        inc, _, _ = smart_csv.csv_open(inf)
        with open(outcsv_name, 'wt') as outf:
            outc = csv.writer(outf)
            outc.writerow(inc.next())

            for row in inc:
                if has_outliers(outliers, row):
                    skipped += 1
                    print row
                else:
                    outc.writerow(row)
                    kept += 1
    print 'kept', kept, 'skipped', skipped

if __name__ == '__main__':
    # txt-file, limit, incsv, outcsv
    kill_outliers(sys.argv[3], sys.argv[4], list(find_outliers(sys.argv[1], int(sys.argv[2]))))
