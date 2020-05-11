import sys
import networkx as nx
import pickle
import os

def removePath(g: nx.Graph, path, path_cap):
    for i in range(0, len(path)-1):
        g[path[i]][path[i+1]]['cap'] -= path_cap

g = nx.Graph()
g.add_nodes_from((1,2,3,4,5,6,7,8))
g.add_edges_from(((1,2), (2,3), (3,4), (2,5), (5,6), (6,4), (1,7), (7,8), (8,3)))

for a, b in g.edges():
    g[a][b]['cap'] = 5
g[1][2]['cap'] = 8
g[2][3]['cap'] = 8
g[3][4]['cap'] = 8

with open('topo/Aaa', 'wb') as fp:
    pickle.dump(g, fp)
