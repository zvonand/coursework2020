#!/usr/bin/env python3

import sys
import networkx as nx
import pickle
from complicated import *



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ('Usage: main.py [topo_file]')
        sys.exit(1)

    with open(sys.argv[1], 'rb') as fp:
        g = pickle.load(fp)

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    print(findPaths(g, 1, 8, 23))
    print(findPaths(g, 1, 8, 33))
