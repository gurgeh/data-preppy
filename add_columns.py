import csv
import sys


def add_columns(incsv_name, outcsv_name, header_loc, headers, callback):
    with open(incsv_name) as inf:
        cin = csv.reader(inf)
        inheaders = cin.next()
        outheaders = inheaders[:header_loc] + headers + inheaders[header_loc:]
        with open(outcsv_name, 'wt') as outf:
            cout = csv.writer(outf)
            cout.writerow(outheaders)
            for row in cin:
                extra = callback(row)
                cout.writerow(row[:header_loc] + extra + row[header_loc:])


def add_csv(incsv_name_base, incsv_name_new, outcsv_name, new_loc, id_col=0):
    id_col = int(id_col)
    new_loc = int(new_loc)

    with open(incsv_name_new) as inf:
        cin = csv.reader(inf)
        headers = cin.next()
        print 'id_col is', headers[id_col]
        del headers[id_col]

        global stopped, cur_row
        stopped = False
        empty_row = [''] * len(headers)
        cur_row = empty_row + ['']

        def match_id(row):
            global stopped, cur_row
            while not stopped and cur_row[id_col] < row[0]:
                try:
                    cur_row = cin.next()
                except StopIteration:
                    stopped = True
            if stopped:
                return empty_row

            if row[0] == cur_row[id_col]:
                cur_row2 = cur_row[:]
                del cur_row2[id_col]
                return cur_row2
            return empty_row

        add_columns(incsv_name_base, outcsv_name, new_loc, headers, match_id)


def add_csv_rows(incsv_name_base, incsv_name_new, outcsv_name, new_loc, id_col=0):
    new_loc = int(new_loc)
    id_col = int(id_col)
    with open(incsv_name_base) as inf1:
        cin1 = csv.reader(inf1)
        headers1 = cin1.next()
        with open(incsv_name_new) as inf2:
            cin2 = csv.reader(inf2)
            headers2 = cin2.next()
            print 'id_col is', headers2[id_col]
            del headers2[id_col]
            with open(outcsv_name, 'wt') as outf:
                outheaders = headers1[:new_loc] + headers2 + headers1[new_loc:]
                cout = csv.writer(outf)
                cout.writerow(outheaders)
                for row1 in cin1:
                    row2 = cin2.next()
                    del row2[id_col]
                    cout.writerow(row1[:new_loc] + row2 + row1[new_loc:])


if __name__ == '__main__':
    add_csv_rows(*sys.argv[1:])
