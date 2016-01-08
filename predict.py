import sys
import csv

import pandas
import numpy as np

try:
    from sknn.mlp import Regressor, Layer, Classifier
except ImportError:
    pass

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn import tree

NAMES = {'Tree': 'Decision Tree',
         'NN': 'Neural Network'}


def get_XY(fname):
    xs = pandas.read_csv(fname)
    Y = xs.values[:, -1]
    X = np.delete(xs.values, [xs.values.shape[1] - 1], 1)
    return X, Y, xs.columns.values


def NN(X, Y, outname, headers, classify=True):
    import logging

    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG,
        stream=sys.stdout)

    if classify:
        nn = Classifier(
            layers=[
                Layer("Maxout", units=10, pieces=2),
                Layer("Softmax")],
            learning_rate=0.001,
            verbose=True,
            n_iter=25)
    else:
        nn = Regressor(
            layers=[
                Layer("Rectifier", units=10),
                Layer("Linear")],
            learning_rate=0.02,
            verbose=True,
            n_iter=10)

    pipeline = Pipeline([
        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
        ('neural network', nn)])

    try:
        pipeline.fit(X, Y)
    except KeyboardInterrupt:
        pass
    print pipeline.score(X, Y)

    # with open(outname, 'w') as fout:
    #    cPickle.dump(pipeline, fout)

    return pipeline


def Tree(X, Y, outname, headers):
    clf = tree.DecisionTreeClassifier(
        max_leaf_nodes=20
    )
    clf.fit(X, Y)
    print clf.score(X, Y)

    # with open(outname, 'w') as fout:
    #    cPickle.dump(clf, fout)
    visualize_tree(clf, outname + '_tree.pdf', headers)

    return clf


def visualize_tree(clf, outname, headers):
    from sklearn.externals.six import StringIO
    import pydot
    dot_data = StringIO()
    tree.export_graphviz(clf, out_file=dot_data, feature_names=list(headers))
    graph = pydot.graph_from_dot_data(dot_data.getvalue().decode('latin1').encode('utf8'))
    graph.write_pdf(outname)


def write_score(Z, outname, cidname, colname):
    with open(cidname) as cids:
        cin = csv.reader(cids)
        print cin.next()
        with open(outname, 'wt') as fout:
            cout = csv.writer(fout)
            cout.writerow(['KundID', colname])
            for a in Z:
                x = cin.next()
                cid = x[0]
                try:
                    a0 = a[0]
                except IndexError:
                    a0 = a
                cout.writerow([cid, a0])


if __name__ == '__main__':
    method = sys.argv[1]
    mname = NAMES[method]

    full_file = sys.argv[2]
    basefile = full_file[:-4]
    full_cidfile = sys.argv[3]
    outbase = sys.argv[4]
    colname = sys.argv[5]

    X, Y, headers = get_XY(basefile + '_train.csv')
    pp = eval(method)(X, Y, basefile, headers)
    del X, Y

    import metrics
    metrics.metric(pp, basefile + '_test.csv', '../data/%s' % mname)

    X, Y, headers = get_XY(full_file)
    Z = pp.predict(X)
    write_score(Z, outbase + '%s - Score.csv' % mname, full_cidfile, colname)
