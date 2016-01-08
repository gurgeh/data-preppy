import csv
import sys

column_filename = sys.argv[1]
columns = []


def filter_columns(colname, incsvname, outcsvname):
    with open(colname, 'rb') as columnfile:
        i = 0
        for row in columnfile:
            if row.split(',')[0].strip()[:1] == '+':
                columns.append(i)
            i += 1

    with open(incsvname, 'rb') as incsvfile:
        with open(outcsvname, 'wb') as outcsvfile:
            csvreader = csv.reader(incsvfile)
            csvwriter = csv.writer(outcsvfile)
            headers = csvreader.next()
            headerline = [headers[c] for c in columns]
            csvwriter.writerow(headerline)
            for row in csvreader:
                csvwriter.writerow([row[c] for c in columns])

if __name__ == '__main__':
    filter_columns(*sys.argv[1:])
