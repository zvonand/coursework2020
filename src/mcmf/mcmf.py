import sys
import networkx as nx
import pickle
import copy

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

def maxFlowWoPath(g: nx.Graph, path, path_cap=-1):
    if path_cap == -1:
        path_cap = pathCapacity(g, path)
    removePath(g, path, path_cap)
    flow = nx.maximum_flow(g, path[0], path[-1], capacity='cap')[0]
    addPath(g, path, path_cap)
    return flow

def pathCost(g: nx.Graph, path):
    max_cap = pathCapacity(g, path)
    if max_cap == 0:
        return -1
    flow_with = nx.maximum_flow(g, path[0], path[-1], capacity='cap')[0]
    flow_without = maxFlowWoPath(g, path, max_cap)
    #print(f'path: {path},  overload cost: {(flow_with - flow_without - max_cap)*100//max_cap}, len cost: {len(path)*10//g.number_of_nodes()}')
    return (flow_with - flow_without - max_cap)*100//max_cap + len(path)*10//g.number_of_nodes()

def removeCycles(path):
    i = 0
    while i < len(path):
        if path[i] in path[i+1:]:
            j = len(path) - 1
            while path[j] != path[i]:
                j -= 1
            for k in range(i+1, j+1):
                del path[i+1]
        i += 1
    return path


def getNPaths(g: nx.Graph, fr, to, path_num: int):
    graph = copy.deepcopy(g)
    size = graph.number_of_nodes()
    max_node = size+1
    edges = list(graph.edges)
    for a, b in edges:
        mul = 0
        if graph[a][b]['cap'] != 0:
            mul = 1000 / graph[a][b]['cap']
            graph[a][b]['cap'] = 1
        for i in range(1, path_num):
            graph.add_edge(a, max_node + i - 1, cap=1, weight=(i+1)*mul)
            graph.add_edge(max_node + i - 1, b, cap=1, weight=0)
        max_node += path_num - 1

    sink = graph.number_of_nodes()+1
    graph.add_edge(to, sink, cap=path_num)
    mfmc = nx.max_flow_min_cost(graph, fr, sink, capacity='cap', weight='wt')
    paths = []
    finish = to

    for counter in range(path_num):
        i = fr
        path = [fr]
        while i != finish:
            for key, value in mfmc[i].items():
                if value == 1:
                    mfmc[i][key] = 0
                    path.append(key)
                    i = key
                    break

        pth = []
        for elem in path:
            if elem <= size:
                pth.append(elem)

        pth = removeCycles(pth)

        if not pth in paths:
            paths.append(pth)
    return paths

def balanceCapacities(g: nx.Graph, paths, req):
    ret = {}
    cap = 0
    while paths != []:
        if (cap == req):
            break
        path = min(paths, key=lambda x: pathCost(g, x))
        pc = pathCapacity(g, path)
        ret[tuple(path)] = min(pc, req-cap)
        cap += ret[tuple(path)]
        removePath(g, path, ret[tuple(path)])
        paths.remove(path)
    if cap < req:
        return {}

    ret1 = {}
    for k in ret.keys():
        if ret[k] != 0:
            #print (ret[k])
            ret1[k] = ret[k]
    return ret1


def findPaths(g: nx.Graph, fr, to, req = 10):
    mf = nx.maximum_flow(g, fr, to, capacity='cap')[0]
    if req > mf or req == 0:
        return {}
    p = 3
    ret = {}
    pr_paths = []
    paths = [0]
    while ret == {} and pr_paths != paths:
        for k in ret.keys():
            addPath(g, k, ret[k])
            del ret[k]
        paths = getNPaths(g, fr, to, p)
        pr_paths = paths
        p += 1
        ret = balanceCapacities(g, paths, req)
    return ret
