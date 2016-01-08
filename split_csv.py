import csv
import sys

from hashlib import md5


def split_csv(inname, outname):
    with open(inname) as inf:
        cin = csv.reader(inf)
        headers = cin.next()
        with open(outname % 'train', 'wt') as outf1:
            cout1 = csv.writer(outf1)
            cout1.writerow(headers)
            with open(outname % 'test', 'wt') as outf2:
                cout2 = csv.writer(outf2)
                cout2.writerow(headers)
                for row in cin:
                    num = ord(md5(''.join(row)).digest()[-1])
                    if num % 2 == 0:
                        cout1.writerow(row)
                    else:
                        cout2.writerow(row)


if __name__ == '__main__':
    split_csv(*sys.argv[1:])
