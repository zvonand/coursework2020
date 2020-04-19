import sys
import random as rd
import networkx as nx
import pickle
import os

tp =  'Abvt'
with open('topo_wcap/' + tp, 'rb') as fp:
    g = pickle.load(fp)

if isinstance(g, nx.MultiGraph):
    print('Warning: graph was converted from MultiGraph to Graph')
    g = nx.Graph(g)
