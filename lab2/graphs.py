#!/usr/bin/env python3

import pickle
import random
from copy import deepcopy

import networkx as nx
from matplotlib import pyplot as plt


class Graph:
    # undirected
    # unweighted
    # nodes: int

    def __init__(self, src=None, allow_self_loops=False):
        if src is None:
            src = dict()
        self.graph = src.copy()
        self.allow_self_loops = allow_self_loops

    def __len__(self):
        return len(self.graph.keys())

    def nodes(self):
        return self.graph.keys()

    # ---------------- Basic modification utils ---------------- #

    def add_edge(self, a, b):
        g = self.graph
        if a not in g.keys() or b not in g.keys():
            raise ValueError("Nodes are not present in graph")
        if b in g[a] or a in g[b]:
            raise ValueError("Nodes are already connected")
        if a == b and not self.allow_self_loops:
            raise ValueError("Self-loops are not allowed in this configuration")
        g[a].add(b)
        g[b].add(a)

    def add_node(self, a):
        g = self.graph
        if a not in g.keys():
            g[a] = set()
        else:
            raise ValueError("Node is already present in graph")

    def rm_edge(self, a, b):
        g = self.graph
        if a not in g.keys() or b not in g.keys():
            raise ValueError("Nodes are not present in graph")
        if a not in g[b] or b not in g[a]:
            raise ValueError("Nodes are not connected")
        g[a].remove(b)
        g[b].remove(a)

    def rm_node(self, a):
        g = self.graph
        if a not in g.keys():
            raise ValueError("Node is not present in graph")
        for b in g[a].copy():
            self.rm_edge(a, b)
        g.pop(a)

    def show(self, path=None):
        if path is None:
            path = list()
        plt.figure(num='Graph view')
        g = nx.Graph(self.graph)
        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos)
        nx.draw_networkx_edge_labels(g, pos, edge_labels={path[i]: i+1 for i in range(len(path))}, font_color='r')
        plt.axis('off')
        plt.show()

    # ---------------- Traverse utils ---------------- #

    def dfs(self, node, visited):
        visited.add(node)
        count = 1
        for i in self.graph[node]:
            if i not in visited:
                count += self.dfs(i, visited)
        return count

    def is_connected(self):
        if len(self) <= 1:
            return True
        visited = set()
        start = random.choice(list(self.graph.keys()))
        self.dfs(start, visited)
        return visited == self.graph.keys()

    # ---------------- Eulerian cycle block ---------------- #

    def is_eulerian(self):
        # checks circuit only, does not count path
        if not self.is_connected():
            return False
        g = self.graph
        for node in g.keys():
            if len(g[node]) % 2 == 1:
                return False
        return True

    def is_bridge(self, a, b):
        g = self.graph
        if len(g[a]) == 1:
            return False
        visited = set()
        c1 = self.dfs(a, visited)
        self.rm_edge(a, b)
        visited = set()
        c2 = self.dfs(a, visited)
        self.add_edge(a, b)
        return c1 > c2

    def _eulerian_cycle_iter(self, path, start=None):
        if start is None:
            start = random.choice(list(self.graph.keys()))
        for node in self.graph[start]:
            if not self.is_bridge(start, node):
                path.append((start, node))
                self.rm_edge(start, node)
                self._eulerian_cycle_iter(path, node)

    def get_eulerian_cycle(self):
        if not self.is_eulerian():
            return None
        path = list()
        g2 = Graph(deepcopy(self.graph))
        g2._eulerian_cycle_iter(path)
        return path

    # ---------------- Hamiltonian cycle block ---------------- #

    def _ham_valid_edge(self, ind, b, path):
        if b not in self.graph[path[ind-1]]:
            return False
        return b not in path

    def _ham_util_cycle(self, ind, path):
        if ind == len(self):
            return path[0] in self.graph[path[ind-1]]
        for nxt in self.graph.keys():
            if self._ham_valid_edge(ind, nxt, path):
                path[ind] = nxt
                if self._ham_util_cycle(ind+1, path):
                    return True
                path[ind] = None
        return False

    def get_hamiltonian_cycle(self, start=None):
        if start is None:
            start = random.choice(list(self.graph.keys()))
        path = [None]*(len(self)+1)
        path[0] = path[-1] = start
        if self._ham_util_cycle(1, path):
            return [(path[i], path[i+1]) for i in range(len(path)-1)]
        return None

    # ---------------- File I/O for graph ----------------

    @staticmethod
    def load(filename):
        # Warning: vulnerable method! Only trusted files should be loaded.
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except IOError as e:
            raise e(f"Pickle could not load graph from {filename}")

    @staticmethod
    def save(obj, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(obj, f)
        except IOError as e:
            raise e(f"Pickle could not write graph to {filename}")

    # ---------------- Graph generator ----------------

    @staticmethod
    def generate(nodes_count, density=0.25):
        g = Graph()
        i = 0
        while i < nodes_count:
            try:
                g.add_node(random.randint(1, 64 * nodes_count))
                i += 1
            except ValueError:
                continue
        edges_count = int(nodes_count * (nodes_count - 1) * density / 2)
        i = 0
        free_nodes = set(g.nodes()).copy()
        while i < edges_count and free_nodes:
            try:
                a = random.choice(list(free_nodes))
                if len(g.graph[a]) + 1 >= len(g):
                    free_nodes.remove(a)
                    continue
                b = random.choice(list(g.nodes() - {a, } - g.graph[a]))
                g.add_edge(a, b)
                i += 1
            except ValueError:
                continue
        return g
