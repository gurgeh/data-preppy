import csv
import sys

import pandas as pd

from sklearn import cluster
from numpy.linalg import norm


"""
group = cc.mb.predict(cc.df)
cluster_csv.output_cluster(cc.mb, group, '1.csv', '2.csv')
"""


class ClusterCSV:

    def __init__(self, fname='../data/filtered_fixed.csv'):
        self.fname = fname
        print 'reading data'
        self.df = pd.read_csv(fname)

        self.df.drop(self.df.columns[[-2, -1]], axis=1, inplace=True)

        self.dfmin = self.df.min()
        self.dfmax = self.df.max()
        # olddf = self.df.copy()
        self.df -= self.dfmin
        self.df /= self.dfmax
        print 'clustering'
        self.mb = cluster.KMeans(5, precompute_distances=True, n_jobs=-1, verbose=True)
        self.mb.fit(self.df.values)

        for c in self.mb.cluster_centers_:
            k = self.find_nearest(c)
            print k

    def find_nearest(self, centroid):
        best = 1000000000
        for i in xrange(len(self.df)):
            x = norm(self.df.iloc[i].values - centroid)
            if x < best:
                besti = i
                best = x
        return besti


def get_idmap(cname):
    idmap = {}
    with open(cname) as f:
        c = csv.reader(f)
        idname = c.next()[0]
        i = 0
        for row in c:
            idmap[i] = row[0]
            i += 1

    return idmap, idname


def output_cluster(mb, group, outcsv_name, idcsv_name):
    idmap, id_name = get_idmap(idcsv_name)
    with open(outcsv_name, 'wt') as outf:
        cout = csv.writer(outf)
        cout.writerow([id_name] + ['cluster_%d' % n for n in range(5)])
        for i, clust in enumerate(group):
            cid = idmap[i]
            cout.writerow([cid] + ['1' if clust == j else '0' for j in range(5)])

if __name__ == '__main__':
    incsv = sys.argv[1]
    outcsv = sys.argv[2]
    cc = ClusterCSV(incsv)
    group = cc.mb.predict(cc.df)
    output_cluster(cc.mb, group, outcsv, '/vboxshare/VFinans/RESPONSFLAGGOR_AVPERS.csv')
