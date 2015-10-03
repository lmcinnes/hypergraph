# -*- coding: utf-8 -*-
"""
hypergraph.hypergraph: Basic hypergraph class.
"""
# Author: Leland McInnes <leland.mcinnes@gmail.com>
#
# License: LGPL v2 

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
    	'''Return a list (or iterable in python3) of the node
    	objects of the hypergraph.
    	'''
        return self.node.keys()

    def edges(self):
    	'''Return a list (or iterable in python3) of the edge
    	objects of the hypergraph.
    	'''
         return self.edge.keys()

	def add_node(self, new_node):
		'''Add a new node to the hypergraph.

		Parameters
		----------

		new_node : object
			The new node to add to the hypergraph
		'''
		self.nodes[new_node] = POMSet([])

	def add_edge(self, new_edge, edge_labels, edge_order=None):
		'''Add a new edge to the hypergraph.

		Parameters
		----------
		new_edge : object
			The edge object to add to the hypergraph.

		edge_labels : iterable
			An iterable of node objects that the edge relates.
			If the objects are not already nodes of the hypergraph
			then new nodes will be added to the hypergraph for them.

		edge_order : numpy ndarray (len(edge_labels), len(edge_labels)), optional
			The POMSET order of the edge, or None. If None the
			edge will be undirected (but can have dependencies added).
			(default None)
		'''
		self.edges[new_edge] = POMSet(edge_labels, edge_order)

		for node in edge_labels:
			if node not in self.nodes:
				self.add_node(node)
			self.nodes[node].add_label(new_edge)

	def dual(self):
		'''Return a new hypergraph that is the dual of the current
		hypergraph.
		'''
		result = Hypergraph()
		result.nodes = self.edges.copy()
		result.edges = self.nodes.copy()
		return result

	def networkx_bipartite_representation(self):
		'''Return a NetworkX graph of the bipartite representation of the 
		hypergraph.
		'''
		result = nx.Graph()
		result.add_nodes_from(self.nodes.keys() + self.edges.keys())
		for edge in self.edges:
			for label in self.edges[edge].labels:
				result.add_edge(edge, label)

		return result

	def networkx_undirected_cliquification(self):
		'''Return a NetworkX graph derived from the hypergraph by
		converting all hyperegdes into graph cliques.
		'''
		result = nx.Graph()
		result.add_nodes_from(self.nodes.keys())
		for edge in self.edges:
			for n1, n2 in itr.combinations(self.edges[edge].labels, 2):
				result.add_edge(n1, n2)

		return result
