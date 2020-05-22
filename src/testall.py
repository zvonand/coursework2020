#!/usr/bin/env python3

import sys
import os
import networkx as nx
import pickle
import complicated
import prec_paths.algo as pp
import prec_wts.algo as pw
import mcmf
import signal

class Timeout(Exception):
    pass

def handler(sig, frame):
    raise Timeout

signal.signal(signal.SIGALRM, handler)

files = []
for tp in os.listdir('edge_weights/'):
    files.append(tp)

files.sort()

for tp in files:
    with open('edge_weights/' + tp, 'rb') as fp:
        g = pickle.load(fp)

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    #print ("{:25s}   nodes: {:3d}   time: ".format(sys.argv[1], g.number_of_nodes()))
    succeeded, failed, tout = 0, 0, 0
    nodes_lst = list(g.nodes)
    for i in range(len(nodes_lst)-1):
        for j in range(i+1, len(nodes_lst)):
            paths = []
            mf = nx.maximum_flow(g, nodes_lst[i], nodes_lst[j], capacity='cap')[0]
            a, b = nodes_lst[i], nodes_lst[j]

            signal.signal(signal.SIGALRM, handler)
            signal.alarm(5)
            try:
                paths = mcmf.findPaths(g, a, b, mf)
                if paths != {}:
                    succeeded += 1
                else:
                    failed += 1
                    #print(f'fail at {tp}, from {a} to {b}')
                for key in paths.keys():
                    mcmf.addPath(g, key, paths[key])
            except Timeout:
                tout += 1

    print(f'{tp}; succeeded: {succeeded}, failed: {failed}, timed out: {tout}')
    #print(complicated.findPaths(g, 1, 4, 9))
