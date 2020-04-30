import sys
import random as rd
import networkx as nx
import pickle
import os

rd.seed()
for tp in os.listdir('topo/'):
#tp =  'Abvt'
    with open('topo/' + tp, 'rb') as fp:
        g = pickle.load(fp)

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    filled = []

    newg = nx.Graph()

    for v1 in g.edge.keys():
        for v2 in g.edge[v1].keys():
            if (v2, v1) not in filled:
                newg.add_edge(v1, v2)
                newg[v1][v2]['cap'] = rd.randrange(1, 100)
                newg[v1][v2]['wt'] = 1
                newg[v2][v1]['cap'] = newg[v1][v2]['cap']
                newg[v2][v1]['wt'] = 1
                filled.append((v1, v2))

    with open('topo/' + tp, 'wb') as fp:
        pickle.dump(newg, fp)
