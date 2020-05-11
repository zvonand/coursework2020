import sys
import random as rd
import networkx as nx
import pickle
import os
from timeit import timeit

def removePath(g: nx.Graph, path, path_cap):
    for i in range(0, len(path)-1):
        g[path[i]][path[i+1]]['cap'] -= path_cap


tp =  'Aaa'
with open('topo/' + tp, 'rb') as fp:
    g = pickle.load(fp)

if isinstance(g, nx.MultiGraph):
    print('Warning: graph was converted from MultiGraph to Graph')
    g = nx.Graph(g)
