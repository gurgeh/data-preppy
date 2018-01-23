import csv
import os
import sys


def add_all(path, prefix):
    rows = []
    first = True
    for fname in os.listdir(path):
        if fname.startswith(prefix):
            with open(fname) as inf:
                c = csv.reader(inf)
                if not first: # remove header from every file, but the first
                    c.next() # remove header
                first = False
                rows.extend(c)
    return rows

if __name__ == '__main__':
    add_all(*sys.argv[1:])
