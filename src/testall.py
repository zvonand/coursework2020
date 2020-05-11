#!/usr/bin/env python3

import sys
import os
import networkx as nx
import pickle
import complicated
import on_weights

files = []
for tp in os.listdir('path_weights/'):
    files.append(tp)

files.sort()

for tp in files:
    with open('topo/' + tp, 'rb') as fp:
        g = pickle.load(fp)

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    #print ("{:25s}   nodes: {:3d}   time: ".format(sys.argv[1], g.number_of_nodes()))
    succeeded, failed = 0, 0
    nodes_lst = list(g.nodes)
    for i in range(len(nodes_lst)-1):
        for j in range(i+1, len(nodes_lst)):
            with open('topo/' + tp, 'rb') as fp:
                g = pickle.load(fp)
            a, b = nodes_lst[i], nodes_lst[j]
            if on_weights.findPaths(tp, g, a, b) != {}:
                succeeded += 1
            else:
                failed += 1
                print(f'fail at {tp}, from {a} to {b}')
    print(f'{tp}; succeeded: {succeeded}, failed: {failed}')
    #print(complicated.findPaths(g, 1, 4, 9))
