import sys
import random as rd
import networkx as nx
import pickle
import os

def pathCost(g: nx.Graph, path):
    if len(path) <= 1:
        return 0
    weight = 0
    for i in range(len(path)-1):
        weight += g[path[i]][path[i+1]]['wt']
    return weight

def pathCapacity(g: nx.Graph, path):
    if len(path) <= 1:
        return 0
    capacity = g[path[0]][path[1]]['cap']
    for i in range(1, len(path)-1):
        link_cap =  g[path[i]][path[i+1]]['cap']
        if link_cap < capacity:
            capacity = link_cap
    return capacity


tp =  'Abvt'
with open('topo/' + tp, 'rb') as fp:
    g = pickle.load(fp)

if isinstance(g, nx.MultiGraph):
    print('Warning: graph was converted from MultiGraph to Graph')
    g = nx.Graph(g)
