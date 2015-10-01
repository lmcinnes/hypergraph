# -*- coding: utf-8 -*-
"""
hypergraph.hypergraph: Basic hypergraph class.
"""
# Author: Leland McInnes <leland.mcinnes@gmail.com>
#
# License: GPL v2 

import networkx as nx
import itertools as itr

class Hypergraph (object):

	node = {}
	edge = {}

	def __init__(self, nodes=None):
		if nodes is not None:
			for node in nodes:
				self.nodes[node] = POMSet([])

        def nodes(self):
                return self.node.keys()

        def edges(self):
                return self.edge.keys()

	def add_node(self, new_node):
		self.nodes[new_node] = POMSet([])

	def add_edge(self, new_edge, edge_labels, edge_order=None):
		self.edges[new_edge] = POMSet(edge_labels, edge_order)

		for node in edge_labels:
			if node not in self.nodes:
				self.add_node(node)
			self.nodes[node].add_label(new_edge)

	def dual(self):
		result = Hypergraph()
		result.nodes = self.edges.copy()
		result.edges = self.nodes.copy()
		return result

	def networkx_bipartite_representation(self):
		result = nx.Graph()
		result.add_nodes_from(self.nodes.keys() + self.edges.keys())
		for edge in self.edges:
			for label in self.edges[edge].labels:
				result.add_edge(edge, label)

		return result

	def networkx_undirected_two_section(self):
		result = nx.Graph()
		result.add_nodes_from(self.nodes.keys())
		for edge in self.edges:
			for n1, n2 in itr.combinations(self.edges[edge].labels, 2):
				result.add_edge(n1, n2)

		return result
