import sys
import random as rd
import networkx as nx
import pickle
import os

rd.seed()
for tp in os.listdir('topo_wcap/'):
#tp =  'Abvt'
    with open('topo_wcap/' + tp, 'rb') as fp:
        g = pickle.load(fp)

    if isinstance(g, nx.MultiGraph):
        print('Warning: graph was converted from MultiGraph to Graph')
        g = nx.Graph(g)

    filled = []

    for v1 in g.edge.keys():
        for v2 in g.edge[v1].keys():
            if (v2, v1) not in filled:
                g.edge[v1][v2]['cap'] = rd.randrange(1, 100)
                g.edge[v1][v2]['wt'] = 1
                g.edge[v2][v1]['cap'] = g.edge[v1][v2]['cap']
                g.edge[v2][v1]['wt'] = 1
                filled.append((v1, v2))

    with open('topo_wcap/' + tp, 'wb') as fp:
        pickle.dump(g, fp)
