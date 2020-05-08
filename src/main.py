#!/usr/bin/env python3

import sys
import networkx as nx
import pickle
import complicated


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ('Usage: main.py [topo_file]')
        sys.exit(1)

    with open(sys.argv[1], 'rb') as fp:
        g = pickle.load(fp)

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    #print ("{:25s}   nodes: {:3d}   time: ".format(sys.argv[1], g.number_of_nodes()))
    print(complicated.findPaths(g, 1, 4, 60))
