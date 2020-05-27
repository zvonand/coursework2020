#!/usr/bin/env python3

import sys
import os
import networkx as nx
import pickle
import prec_paths.algo as pp
import prec_wts.algo as pw
import mcmf.mcmf as mcmf
import signal
import random as rd
import collections


class Timeout(Exception):
    pass

def handler(sig, frame):
    raise Timeout

def commonEdges(p1, p2):
    count = 0
    for i in range(len(p1) - 1):
        for j in range(len(p2) - 1):
            if (p2[j] == p1[i] and p2[j+1] == p1[i+1]) or (p2[j] == p1[i+1] and p2[j+1] == p1[i]):
                count += 1
    return count

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

def maxFlowWoPath(g: nx.Graph, path, path_cap):
    removePath(g, path, path_cap)
    flow = nx.maximum_flow(g, path[0], path[-1], capacity='cap')[0]
    addPath(g, path, path_cap)
    return flow

def pathCost(g: nx.Graph, path):
    max_cap = pathCapacity(g, path)
    flow_with = nx.maximum_flow(g, path[0], path[-1], capacity='cap')[0]
    flow_without = maxFlowWoPath(g, path, max_cap)
    return (flow_with - flow_without)*100 // max_cap + len(path) * 100 // g.number_of_nodes()

def groupCost(g: nx.Graph, paths):
    cost = 0
    for path in paths.keys():
        addPath(g, path, paths[path])
        cost += pathCost(g, path)
        removePath(g, path, paths[path])
    ks = list(paths.keys())
    for i in range(len(ks)-1):
        for j in range(i+1, len(ks)):
            cost += 100 * commonEdges(ks[i], ks[j])
    return cost


signal.signal(signal.SIGALRM, handler)

files = []
for tp in os.listdir('topo/'):
    files.append(tp)

files.sort()
succs = []

dc = {'m': {i: [] for i in range(11)},  'p': {i: [] for i in range(11)}, 'w': {i: [] for i in range(11)}}

suc = {'m': {i: 0 for i in range(11)}, 'p': {i: 0 for i in range(11)}, 'w': {i: 0 for i in range(11)}}
fail = {'m': {i: 0 for i in range(11)}, 'p': {i: 0 for i in range(11)}, 'w': {i: 0 for i in range(11)}}

# suc = {'m': 0, 'p': 0, 'w': 0}
# fail = {'m': 0, 'p': 0, 'w': 0}

for tp in files:
    if tp not in os.listdir('path_weights/') or tp not in os.listdir('edge_weights/'):
        continue
    with open('topo/' + tp, 'rb') as fp:
        m = pickle.load(fp)
    with open('topo/' + tp, 'rb') as fp:
        w = pickle.load(fp)
    with open('topo/' + tp, 'rb') as fp:
        p = pickle.load(fp)
    print(f'Processing: {tp}')

    if isinstance(m, nx.MultiGraph):
        m = nx.Graph(m)
        w = nx.Graph(w)
        p = nx.Graph(p)

    edges, nodes = m.number_of_edges(), m.number_of_nodes()
    mn, wn, pn = 0, 0, 0

    for iter in range(1000):
        a, b = 0, 0
        while a == b:
            if 0 not in m.nodes:
                a = rd.randrange(nodes) + 1
                b = rd.randrange(nodes) + 1
            else:
                a = rd.randrange(nodes)
                b = rd.randrange(nodes)
        mfs = {'m': nx.maximum_flow(m, a, b, capacity='cap')[0], 'p': nx.maximum_flow(p, a, b, capacity='cap')[0], 'w': nx.maximum_flow(w, a, b, capacity='cap')[0]}
        mf = min(mfs.values())
        req = mf if mf <= 2 else rd.randrange(mf//2, mf)
        if not req:
            continue

        m_paths, p_paths, w_paths = [], [], []
        m_cost, p_cost, w_cost = 0, 0, 0
        signal.alarm(5)
        try:
            m_paths = mcmf.findPaths(m, a, b, req)
            p_paths = pp.findPaths(tp, p, a, b, req)
            w_paths = pw.findPaths(tp, w, a, b, req)

            if m_paths != {}:
                suc['m'][10*req//mfs['m']] += 1
                m_cost = groupCost(m, m_paths)
                dc['m'][10*req//mfs['m']].append(m_cost)
            else:
                fail['m'][10*req//mfs['m']] += 1

            if w_paths != {}:
                suc['w'][10*req//mfs['w']] += 1
                w_cost = groupCost(w, w_paths)
                dc['w'][10*req//mfs['w']].append(w_cost)
            else:
                fail['w'][10*req//mfs['w']] += 1

            if p_paths != {}:
                suc['p'][10*req//mfs['p']] += 1
                p_cost = groupCost(p, p_paths)
                dc['p'][10*req//mfs['w']].append(p_cost)
            else:
                fail['p'][10*req//mfs['p']] += 1

        except Timeout:
            print('Timed out')

with open('test_res', 'wb') as fp:
    pickle.dump(dc, fp)
print ("Succ: mf: ", [suc['m'][i]*100//(suc['m'][i]+fail['m'][i]) for i in range(11)])
print ("Succ: pp: ", [suc['p'][i]*100//(suc['p'][i]+fail['p'][i]) for i in range(11)])
print ("Succ: pw: ", [suc['w'][i]*100//(suc['w'][i]+fail['w'][i]) for i in range(11)])
