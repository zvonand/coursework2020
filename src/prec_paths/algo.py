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


def getNextPath(g: nx.Graph, candidates):
    return min(candidates.keys(), key=lambda x: candidates[x])

def commonEdges(p1, p2):
    count = 0
    for i in range(len(p1) - 1):
        for j in range(len(p2) - 1):
            if (p2[j] == p1[i] and p2[j+1] == p1[i+1]) or (p2[j] == p1[i+1] and p2[j+1] == p1[i]):
                count += 1
    return count

def maxFlowWoPath(g: nx.Graph, path, path_cap):
    removePath(g, path, path_cap)
    flow = nx.maximum_flow(g, path[0], path[-1], capacity='cap')[0]
    addPath(g, path, path_cap)
    return flow

def pathCost(g: nx.Graph, path):
    max_cap = pathCapacity(g, path)
    flow_with = nx.maximum_flow(g, path[0], path[-1], capacity='cap')[0]
    flow_without = maxFlowWoPath(g, path, max_cap)
    #print(f'overload cost: {(flow_with - flow_without - max_cap)*100 // max_cap}, length cost: {len(path) * 10 // g.number_of_nodes()}')
    return (flow_with - flow_without - max_cap)*100 // max_cap + len(path) * 10 // g.number_of_nodes()


def findPaths(name, g: nx.Graph, fr, to, cap_req=0):
    mf = nx.maximum_flow(g, fr, to, capacity='cap')[0]
    if cap_req == 0:
        cap_req = mf
    elif cap_req > mf:
        return {}
    capacity, cost = 0, 0
    paths = {}
    with open('path_weights/' + name, 'rb') as fp:
        wts = pickle.load(fp)

    req_met = False
    while not req_met:
        if len(wts[tuple(sorted((fr, to)))]) == 0:
            return {}

        path = getNextPath(g, wts[tuple(sorted((fr, to)))])
        #print (pathCost(g, path))
        for k in wts[tuple(sorted((fr, to)))].keys():
            wts[tuple(sorted((fr, to)))][k] += commonEdges(path, k) * 100

        cap = pathCapacity(g, path)
        if cap > (cap_req-capacity):
            cap = cap_req-capacity
        if cap > 0:
            paths[path] = cap
            removePath(g, path, cap)
            capacity += cap
        del wts[tuple(sorted((fr, to)))][path]

        if capacity >= cap_req:
            req_met = True
    return paths
