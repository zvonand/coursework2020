import sys
import random as rd
import networkx as nx
import pickle
import os


def rndOne(tp):
    with open(tp, 'rb') as fp:
        g = pickle.load(fp)
    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    filled = []

    for v1, v2 in g.edges():
        if (v2, v1) not in filled:
            g.add_edge(v1, v2)
            g[v1][v2]['cap'] = rd.randrange(300, 1000)
            g[v1][v2]['wt'] = 1
            g[v2][v1]['cap'] = g[v1][v2]['cap']
            g[v2][v1]['wt'] = 1
            filled.append((v1, v2))

    with open(tp, 'wb') as fp:
        pickle.dump(g, fp)


def rndAll():
    rd.seed()
    for tp in os.listdir('topo/'):
        with open('topo/' + tp, 'rb') as fp:
            g = pickle.load(fp)

        if isinstance(g, nx.MultiGraph):
            print('Warning: graph was converted from MultiGraph to Graph')
            g = nx.Graph(g)

        newg = nx.Graph()

        for v1, v2 in g.edges:
            newg.add_edge(v1, v2)
            newg[v1][v2]['cap'] = rd.randrange(300, 1000)
            newg[v1][v2]['wt'] = 1

        with open('topo/' + tp, 'wb') as fp:
            pickle.dump(newg, fp)

if len(sys.argv) == 2:
    rndOne(sys.argv[1])
else:
    rndAll()
