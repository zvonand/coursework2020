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
import random as rd

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
    try:
        with open('topo/' + tp, 'rb') as fp:
            g = pickle.load(fp)
        with open('edge_weights/' + tp, 'rb') as fp:
            e = pickle.load(fp)
        with open('path_weights/' + tp, 'rb') as fp:
            f = pickle.load(fp)
    except:
        continue

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)
        e = nx.Graph(e)
        f = nx.Graph(f)

    edges, nodes = g.number_of_edges(), g.number_of_nodes()
    #print ("{:25s}   nodes: {:3d}   time: ".format(sys.argv[1], g.number_of_nodes()))
    succeeded, failed, tout = 0, 0, 0
    nodes_lst = list(g.nodes)
    i, j = 0, 0
    while i == j:
        i = rd.randrange(nodes) + 1
        j = rd.randrange(nodes) + 1

    wts, pts, mcmf = True, True, True
    wts_done, pts_done, mcmf_done = 0, 0, 0

    while wts or pts or mcmf:
        mf = nx.maximum_flow(f, nodes_lst[i], nodes_lst[j], capacity='cap')[0]
        req = rd.randrange(mf//10) if mf > 10 else mf
        a, b = nodes_lst[i], nodes_lst[j]

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(8)
        try:
            paths = mcmf.findPaths(g, a, b, mf)
            if paths != {}:
                succeeded += 1
            else:
                failed += 1
            for key in paths.keys():
                mcmf.addPath(g, key, paths[key])
        except Timeout:
            tout += 1
