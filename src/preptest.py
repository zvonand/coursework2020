#!/usr/bin/env python3

import sys
import os
import networkx as nx
import pickle
import complicated
import prec_paths.algo as pp
import prec_wts.algo as pw
import mcmf.mcmf as mcmf
import signal

class Timeout(Exception):
    pass

def handler(sig, frame):
    raise Timeout

signal.signal(signal.SIGALRM, handler)

files = []
for tp in os.listdir('topo/'):
    files.append(tp)

files.sort()
succs = []
for tp in files:
    with open('topo/' + tp, 'rb') as fp:
        g = pickle.load(fp)

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    edges, nodes = g.number_of_edges(), g.number_of_nodes()
    #print ("{:25s}   nodes: {:3d}   time: ".format(sys.argv[1], g.number_of_nodes()))
    succeeded, failed, tout = 0, 0, 0
    nodes_lst = list(g.nodes)
    for i in range(len(nodes_lst)-1):
        for j in range(i+1, len(nodes_lst)):
            mf = nx.maximum_flow(g, nodes_lst[i], nodes_lst[j], capacity='cap')[0]
            a, b = nodes_lst[i], nodes_lst[j]

            signal.signal(signal.SIGALRM, handler)
            signal.alarm(8)
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
    succs.append(((100*succeeded//(succeeded+failed+tout)), 100*tout//(succeeded+failed+tout)))
    print(f'{tp}: {edges} edges, {nodes} nodes; succeeded: {succeeded}, {100 if failed == 0 else 100*succeeded//(succeeded+failed)}%, failed: {failed}, timed out: {tout}')
print (f'Average precision: {sum(succs[0])/len(succs[0])}%, timeouts: {sum(succs[1])/len(succs[1])}')
