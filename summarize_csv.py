#!/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import collections
import calendar
import time

import numpy as np

# from dateutil.parser import parse as dateparse
import smart_csv


def spark(data, bins=10):
    bars = u' ▁▂▃▄▅▆▇█'
    n, _ = np.histogram(data, bins=bins)
    n2 = n * (len(bars) - 1) / (max(n))
    res = u" ".join(bars[i] for i in n2)
    return res.encode('utf8')


def num_str(c, form='%.2f'):
    emptystr = 'empty: %d, ' % c.empties if c.empties else ''
    return ('%%s, %s -> %s, %%s, %%smedian: %s, mean: %%.2f, std: %%.2f' % tuple([form] * 3)) %\
        (c.name, np.amin(c.arr), np.amax(c.arr), spark(c.arr), emptystr, np.median(c.arr),
         np.mean(c.arr), np.std(c.arr))


def kill_dot(x):
    return x
    xs = x.split('.')
    if len(xs) == 1:
        return xs[0]
    if len(xs) > 2:
        return x
    if x[1].replace('0', ''):
        return x
    return x[0]


def date2timestamp(arr):
    return np.array([calendar.timegm(d.tolist().timetuple()) for d in arr], dtype='int64')


def num2date(x):
    return time.strftime('%Y-%m-%d', time.localtime(x))


class DateField:

    def __init__(self, name, size):
        self.name = name
        self.arr = np.array(['2015-07-08 14:12:12.000' for _ in xrange(size)],
                            dtype='datetime64[ms]')
        self.idx = 0
        self.empties = 0

    def add(self, x):
        if x:
            self.arr[self.idx] = np.datetime64(x)
            self.idx += 1
        else:
            self.empties += 1

    def __repr__(self):
        emptystr = 'empty: %d, ' % self.empties if self.empties else ''
        numarr = date2timestamp(self.arr)
        form = "%s"
        return ('%%s, %s -> %s, %%s, %%smedian: %s, mean: %s, std: %%.2f' % tuple([form] * 4)) %\
            (self.name, np.amin(self.arr), np.amax(self.arr), spark(numarr), emptystr, num2date(np.median(numarr)),
             num2date(np.mean(numarr)), np.std(numarr))


class FloatField:

    def __init__(self, name, size):
        self.name = name
        self.arr = np.array(range(size), dtype='float64')
        self.idx = 0
        self.empties = 0

    def add(self, x):
        if x:
            self.arr[self.idx] = x
            self.idx += 1
        else:
            self.empties += 1

    def __repr__(self):
        return num_str(self)


class IntField:

    def __init__(self, name, size):
        self.name = name
        self.arr = np.array(range(size), dtype='int64')
        self.bag = collections.Counter()
        self.idx = 0
        self.empties = 0

    def add(self, x):
        x = kill_dot(x)
        if len(self.bag) <= 1000:
            if x:
                self.bag.update([int(x)])
            else:
                self.bag.update([x])

        if x:
            self.arr[self.idx] = x
            self.idx += 1
        else:
            self.empties += 1

    def __repr__(self):
        return '%s, %s' % (num_str(self, '%d'), self.bag.most_common(10))


class CatField:

    def __init__(self, name):
        self.name = name
        self.bag = collections.Counter()

    def add(self, x):
        self.bag.update([x])

    def __repr__(self):
        return '%s, %d, %s' % (self.name, len(self.bag), self.bag.most_common(10))


class Field:

    def __init__(self, name):
        self.name = name
        self.empties = 0
        self.bools = 0
        self.ints = 0  # ints, not 0 or 1
        self.floats = 0  # floats, not ints
        self.strings = 0  # not numbers or empty
        self.dates = 0

    def to_typed(self):
        allnums = self.floats + self.ints + self.bools
        tot = allnums + self.strings + self.empties + self.dates
        print self.name, self.strings, self.dates, self.empties, self.floats, self.ints, self.bools

        if self.dates:
            others = tot - self.dates - self.empties
            if tot * 0.001 > others > 0:
                print 'Forcing %s to date by removing %d' % (self.name, others)
                allnums = self.strings = self.floats = self.ints = self.bools = 0

        if allnums:
            others = tot - allnums - self.empties
            if tot * 0.001 > others > 0:
                print 'Forcing %s to num by removing %d' % (self.name, others)
                self.dates = self.strings = 0

        if self.strings:
            return CatField(self.name)

        if self.dates and allnums:
            return CatField(self.name)

        if self.floats:
            return FloatField(self.name, allnums)
        if self.ints:
            return IntField(self.name, self.ints + self.bools)
        if self.bools:
            return CatField(self.name)

        if self.dates:
            return DateField(self.name, self.dates)

        if self.empties:
            return CatField(self.name)

        raise AssertionError('This should not happen!')
        return None

    def add(self, x):
        if not x:
            self.empties += 1
        elif x in ['0', '1']:
            self.bools += 1
        elif kill_dot(x).isdigit() and len(kill_dot(x)) < 19:
            self.ints += 1
        else:
            try:
                float(x)
                self.floats += 1
            except ValueError:
                try:
                    d = np.datetime64(x)
                    if type(d) != np.datetime64:
                        print x, d, type(d)
                        raise ValueError
                    self.dates += 1
                except ValueError:
                    self.strings += 1

    def __repr__(self):
        s = []
        if self.empties:
            s.append('empties %d' % self.empties)
        if self.bools:
            s.append('bools %d' % self.bools)
        if self.ints:
            s.append('ints %d' % self.ints)
        if self.floats:
            s.append('floats %d' % self.floats)
        if self.dates:
            s.append('dates %d' % self.dates)
        if self.strings:
            s.append('strings %d' % self.strings)
        return '%s: %s' % (self.name, ', '.join(s))


def main(fname):
    i = 0
    with open(fname, 'rb') as f:
        c, enc, dialect = smart_csv.csv_open(f)
        headers = c.next()
        fields = [Field(h.decode(enc).encode('utf8')) for h in headers[1:]]

        for row in c:
            for val, field in zip(row[1:], fields):
                field.add(val.decode(enc).encode('utf8'))

            i += 1
            if i % 10000 == 0:
                print i

    i = 0
    skips = 0
    with open(fname) as f:
        c, enc, dialect = smart_csv.csv_open(f)
        headers = c.next()
        tfields = [field.to_typed() for field in fields]

        for row in c:
            for val, tfield in zip(row[1:], tfields):
                try:
                    tfield.add(val.decode(enc).encode('utf8'))
                except (ValueError, TypeError):
                    skips += 1
                    print 'Skipping', val, tfield.__class__.__name__
            i += 1
            if i % 10000 == 0:
                print i
        print headers[0].decode(enc)
        for tfield in tfields:
            print tfield

if __name__ == '__main__':
    main(sys.argv[1])
