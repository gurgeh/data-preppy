import sys
import csv

import smart_csv


def read_dict(fname, key, vals):
    d = {}
    with open(fname) as fin:
        c = smart_csv.csv_open(fin)[0]
        headers = c.next()
        keyidx = headers.index(key)
        validx = [headers.index(val) for val in vals]
        for x in c:
            d[x[keyidx]] = [x[i] for i in validx]
    return d


def merge_csv(orig_csv, target_idx, d, key, vals, out_csv, keep):
    with open(orig_csv) as fin:
        cin = smart_csv.csv_open(fin)[0]
        with open(out_csv, 'wt') as fout:
            cout = csv.writer(fout)
            headers = cin.next()
            keyidx = headers.index(key)

            def merge_row(row, vals):
                del row[keyidx]
                return row[:target_idx] + vals + row[target_idx:]

            cout.writerow(merge_row(headers, vals))

            for x in cin:
                cout.writerow(merge_row(x, d.get(x[keyidx], [''] * len(vals))))


if __name__ == '__main__':
    orig_csv = sys.argv[1]
    target_idx = int(sys.argv[2])
    out_csv = sys.argv[3]
    dict_csv = sys.argv[4]
    if sys.argv[5] == 'keep':
        keep = 1
    elif sys.argv[5] == 'kill':
        keep = 0
    else:
        raise ValueError
    key = sys.argv[6]
    vals = sys.argv[7:]

    d = read_dict(dict_csv, key, vals)
    merge_csv(orig_csv, target_idx, d, key, vals, out_csv, keep)
