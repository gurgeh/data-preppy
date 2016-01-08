import csv


def guess_encoding(sample, encodings=('ascii', 'utf8', 'latin1')):
    for encoding in encodings:
        try:
            sample.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            pass
    raise UnicodeDecodeError('No suitable encoding found')


def csv_open(f, verbose=False):
    sample = f.read(1024 * 1024)
    enc = guess_encoding(sample)
    if verbose:
        print enc
    dialect = csv.Sniffer().sniff(sample)
    f.seek(0)
    c = csv.reader(f, dialect)
    return c, enc, dialect
