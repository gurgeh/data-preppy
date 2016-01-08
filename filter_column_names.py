import sys
import csv

import smart_csv


def killf(row, idxs):
    return [x for i, x in enumerate(row) if i not in idxs]


def keepf(row, idxs):
    return [x for i, x in enumerate(row) if i in idxs]


def filter_columns(in_name, out_name, keep, killcols):
    if keep:
        colfilt = keepf
    else:
        colfilt = killf
    with open(in_name) as fin:
        cin = smart_csv.csv_open(fin)[0]
        header = cin.next()
        killidx = set([header.index(k) for k in killcols])
        with open(out_name, 'wt') as fout:
            cout = csv.writer(fout)
            cout.writerow(colfilt(header, killidx))
            for x in cin:
                cout.writerow(colfilt(x, killidx))


if __name__ == '__main__':
    in_name = sys.argv[1]
    out_name = sys.argv[2]
    command = sys.argv[3]
    if command == 'kill':
        keep = False
    elif command == 'keep':
        keep = True
    else:
        raise ValueError

    killcols = sys.argv[4:]

    filter_columns(in_name, out_name, keep, killcols)
