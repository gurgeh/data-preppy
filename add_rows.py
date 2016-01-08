import sys
import csv

import smart_csv


def add_rows(in1, in2, outname):
    with open(in1) as fin1:
        with open(in2) as fin2:
            cin1 = smart_csv.csv_open(fin1)[0]
            cin2 = smart_csv.csv_open(fin2)[0]
            h1 = cin1.next()
            h2 = cin2.next()
            if h1 != h2:
                raise ValueError(str(h1) + ' ' + str(h2))
            with open(outname, 'wt') as fout:
                cout = csv.writer(fout)
                cout.writerow(h1)
                for x in cin1:
                    cout.writerow(x)
                for x in cin2:
                    cout.writerow(x)


if __name__ == '__main__':
    in1 = sys.argv[1]
    in2 = sys.argv[2]
    outname = sys.argv[3]
    add_rows(in1, in2, outname)
