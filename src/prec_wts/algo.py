import sys
import networkx as nx
import pickle

def pathCapacity(g: nx.Graph, path):
    if len(path) <= 1:
        return 0
    capacity = g[path[0]][path[1]]['cap']
    for i in range(1, len(path)-1):
        link_cap =  g[path[i]][path[i+1]]['cap']
        if link_cap < capacity:
            capacity = link_cap
    return capacity

def removePath(g: nx.Graph, path, path_cap):
    for i in range(0, len(path)-1):
        g[path[i]][path[i+1]]['cap'] -= path_cap


def addPath(g: nx.Graph, path, path_cap):
    for i in range(0, len(path)-1):
        g[path[i]][path[i+1]]['cap'] += path_cap

def incrWeights(g: nx.Graph, path):
    for i in range(len(path)-1):
        g[path[i]][path[i+1]]['wt'] += 100

def setWeights(g, wts):
    for k in wts.keys():
        g[k[0]][k[1]]['wt'] = wts[k]

def findPaths(name, g: nx.Graph, fr, to, cap_req=0):
    with open('edge_weights/' + name, 'rb') as fp:
        wts = pickle.load(fp)

    setWeights(g, wts[tuple(sorted((fr,to)))])
    mf = nx.maximum_flow(g, fr, to, capacity='cap')[0]
    if cap_req == 0:
        cap_req = mf
    elif cap_req > mf:
        return {}
    capacity = 0
    paths = {}

    req_met = False
    while not req_met:
        path = nx.shortest_path(g, source=fr, target=to, weight="wt")
        #print(path)
        cap = pathCapacity(g, path)
        if cap >= (cap_req-capacity):
            cap = cap_req-capacity
        if cap > 0:
            paths[tuple(path)] = cap
            removePath(g, path, cap)
            capacity += cap
        else:
            return {}
        incrWeights(g, path)

        if capacity >= cap_req:
         req_met = True
    return paths
