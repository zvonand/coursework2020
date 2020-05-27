import pickle
import collections
import os

files = []
for tp in os.listdir('path_weights/'):
    files.append(tp)

files.sort()

for tp in files:
    with open('path_weights/' + tp, 'rb') as fp:
        wts = pickle.load(fp)
    nw = collections.defaultdict(dict)

    for key in wts.keys():
        nw[tuple(sorted(key))] = wts[key]

    with open('path_weights/' + tp, 'wb') as fp:
        pickle.dump(nw, fp)
