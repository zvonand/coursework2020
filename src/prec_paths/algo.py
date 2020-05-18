import sys
import networkx as nx
import pickle


wts = {}

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


'''
By now, cost is declared as:
    used nodes percentage                   topology overload
(path_length/total_nodes * 100) + (flow_occupance/max_path_capacity * 100)
'''

def getNextPath(g: nx.Graph, candidates):
    return min(candidates.keys(), key=lambda x: candidates[x])


def findPaths(name, g: nx.Graph, fr, to, cap_req=0):
    mf = nx.maximum_flow(g, fr, to, capacity='cap')[0]
    if cap_req == 0:
        cap_req = mf
    elif cap_req > mf:
        print("Denied: no sufficient paths")
        return {}
    capacity, cost = 0, 0
    paths = {}
    with open('path_weights/' + name, 'rb') as fp:
        wts = pickle.load(fp)

    req_met = False
    while not req_met:
        if len(wts[(fr, to)]) == 0:
            return {}

        path = getNextPath(g, wts[(fr, to)])
        cap = pathCapacity(g, path)
        if cap > (cap_req-capacity):
            cap = cap_req-capacity
        if cap > 0:
            paths[path] = cap
            removePath(g, path, cap)
            capacity += cap
        del wts[(fr, to)][path]

        if capacity >= cap_req:
            req_met = True
    return paths
