# -*- coding: utf-8 -*-
"""
hypergraph.hypergraph: Basic hypergraph class.
"""
# Author: Leland McInnes <leland.mcinnes@gmail.com>
#
# License: LGPL v2 

import networkx as nx
import itertools as itr
import numpy as np

from warnings import warn

from collections import Counter, defaultdict
from .pomset import POMSet


class Hypergraph(object):
    """
    A directed hypergraph consisting of nodes as edges. Each node or edge
    is an arbitrary python object, and associated to each node or edge,
    via the `node` and `edge` dictionaries, is a `POMSet` which provides
    a partially ordered multiset of either the nodes contained in an edge,
    or the edges incident upon a node.

    Parameters
    ----------

    nodes : iterable, optional
        An iterable of nodes to initialize the hypergraph with, or None.
        (default None)

    Attributes
    ----------

    node : dict
        A dictionary mapping each node object to its associated POMSet.

    edge : dict
        A dictionary mapping each edge object to its associated POMSet.

    nodes : iterable
        An iterable of all the node objects in the hypergraph.

    edges : iterable
        An iterable of all the edge objects in the hypergraph.
    """

    node = {}
    edge = {}

    def __init__(self, nodes=None):
        if nodes is not None:
            for node in nodes:
                self.node[node] = POMSet([])

    @property
    def nodes(self):
        """Return a list (or iterable in python3) of the node
        objects of the hypergraph.
        """
        return self.node.keys()

    @property
    def edges(self):
        """Return a list (or iterable in python3) of the edge
        objects of the hypergraph.
        """
        return self.edge.keys()

    def neighbors(self, node):
        """Get a set of neighboring nodes.

        Parameters
        ----------

        node : object
            The node to find the neighbors of.

        Returns
        -------

        neighbors : set
            A set of all nodes neighboring the queries node.
        """
        result = set([])
        for edge in self.node[node]:
            result.update(self.edge[edge].labels)
        return result

    def weak_predecessors(self, node):
        """GGet a set of neighboring nodes weakly below the current node
        in any incident edges.

        Parameters
        ----------

        node : object
            The node to find the neighbors of.

        Returns
        -------

        neighbors : set
            A set of all nodes that are weak predecessors of the queries node.
        """
        result = set([])
        for edge in self.node[node]:
            for node_index in range(self.edge[edge].multiplcity()):
                result.update(self.edge[edge].weakly_below(node, node_index))
        return result

    def weak_successors(self, node):
        """Get a set of neighboring nodes weakly above the current node
        in any incident edges.

        Parameters
        ----------

        node : object
            The node to find the neighbors of.

        Returns
        -------

        neighbors : set
            A set of all nodes that are weak successors of the queries node.
        """
        result = set([])
        for edge in self.node[node]:
            for node_index in range(self.edge[edge].multiplcity()):
                result.update(self.edge[edge].weakly_above(node, node_index))
        return result


    def strict_predecessors(self, node):
        """Get a set of neighboring nodes strictly below the current node
        in any incident edges.

        Parameters
        ----------

        node : object
            The node to find the neighbors of.

        Returns
        -------

        neighbors : set
            A set of all nodes that are predecessors to the queries node.
        """
        result = set([])
        for edge in self.node[node]:
            for node_index in range(self.edge[edge].multiplcity()):
                result.update(self.edge[edge].strictly_below(node, node_index))
        return result


    def strict_successors(self, node):
        """Get a set of neighboring nodes strictly above the current node
        in any incident edges.

        Parameters
        ----------

        node : object
            The node to find the neighbors of.

        Returns
        -------

        neighbors : set
            A set of all nodes that are successors to the queries node.
        """
        result = set([])
        for edge in self.node[node]:
            for node_index in range(self.edge[edge].multiplcity()):
                result.update(self.edge[edge].strictly_above(node, node_index))
        return result


    def add_node(self, new_node):
        """Add a new node to the hypergraph.

        Parameters
        ----------

        new_node : object
            The new node to add to the hypergraph
        """
        self.node[new_node] = POMSet([])

    def add_edge(self, new_edge, edge_labels, edge_order=None):
        """Add a new edge to the hypergraph.

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
        """
        self.edge[new_edge] = POMSet(edge_labels, edge_order)

        for node in edge_labels:
            if node not in self.nodes:
                self.add_node(node)
            self.node[node].add_label(new_edge)

    @property
    def dual(self):
        """Return a new hypergraph that is the dual of the current
        hypergraph.

        Returns
        -------

        dual : Hypergraph
            The dual of the hypergraph.
        """
        result = Hypergraph()
        result.node = self.edge.copy()
        result.edge = self.node.copy()
        return result

    @property
    def networkx_bipartite_representation(self):
        """Return a NetworkX graph of the bipartite representation of the
        hypergraph.

        Returns
        -------

        graph : NetworkX Graph
            The bipartite representation graph.
        """
        result = nx.Graph()
        result.add_nodes_from(self.nodes + self.edges)
        for edge in self.edges:
            for label in self.edge[edge].labels:
                result.add_edge(edge, label)

        return result

    @property
    def networkx_undirected_cliquification(self):
        """Return a NetworkX graph derived from the hypergraph by
        converting all hyperedges into graph cliques.

        Returns
        -------

        graph : NetworkX Graph
            The cliquified graph.
        """
        result = nx.Graph()
        result.add_nodes_from(self.nodes)
        for edge in self.edge:
            for n1, n2 in itr.combinations(self.edge[edge].labels, 2):
                result.add_edge(n1, n2)

        return result

    @property
    def networkx_weakly_directed_cliquification(self):
        """Return a NetworkX graph derived from the hypergraph by
        converting hypergraph edges into graph cliques weakly respecting
        directedness  of hyperedges.

        That is, we create a graph edge between node `i` and node `j` if
        there exists a hyperedge that includes nodes `i` and `j` such
        that `j` is greater than or unrelated to `i` in that edge.

        Returns
        -------

        graph : NetworkX Graph
            The cliquified graph.
        """
        result = nx.Graph()
        result.add_nodes_from(self.nodes)
        for edge in self.edge:
            for n1 in self.edge[edge].support:
                for n1_index in range(self.edge[edge].multiplicity(n1)):
                    for n2 in self.edge[edge].weakly_above(n1, n1_index):
                        result.add_edge(n1, n2)

        return result

    @property
    def networkx_strictly_directed_cliquification(self):
        """Return a NetworkX graph derived from the hypergraph by
        converting hypergraph edges into graph cliques strictly respecting
        directedness  of hyperedges.

        That is, we create a graph edge between node `i` and node `j` if
        there exists a hyperedge that includes nodes `i` and `j` such
        that `j` is strictly greater than `i` in that edge.

        Returns
        -------

        graph : NetworkX Graph
            The cliquified graph.
        """
        result = nx.Graph()
        result.add_nodes_from(self.nodes)
        for edge in self.edge:
            for n1 in self.edge[edge].support:
                for n1_index in range(self.edge[edge].multiplicity(n1)):
                    for n2 in self.edge[edge].strictly_above(n1, n1_index):
                        result.add_edge(n1, n2)

        return result

    def _bfs_recursion(self, search_root_list, directed='undirected'):
        next_layer = []
        for node in search_root_list:
            for e in self.node[node]:
                if directed == 'undirected':
                    next_layer.extend(self.edge[e].labels)
                elif directed == 'weakly':
                    next_layer.extend(self.edge[e].weakly_above(node))
                elif directed == 'strictly':
                    next_layer.extend(self.edge[e].strictly_above(node))
                else:
                    ValueError('Directedness must be one of "undirected", weakly", "strictly"')

        if len(next_layer) > 0:
            result = [next_layer, [self._bfs_recursion(next_layer, directed=directed)]]
        else:
            result = [next_layer]

        return result

    def breadth_first_search(self, root, directed='undirected'):
        """Return a nested list representing the breadth first search of the
        hypergraph beginning at node `root`.
        """
        result = [[root], self._bfs_recursion([root], directed=directed)]
        return result

    @property
    def undirected_size_distribution_matrix(self):
        """Return a matrix of size distributions (per node) where the
        (i, j)th entry is number of nodes with i edges of size j
        incident on the node.

        Returns
        -------

        dist_matrix : numpy ndarray
            The size distribution matrix
        """
        result_dict = defaultdict(int)
        for node in self.nodes:
            sizes = Counter(self.edge[e].size for e in self.node[node].labels)
            for i in sizes:
                j = sizes[i]
                result_dict[(i, j)] += 1

        matrix_dimensions = np.array(result_dict.keys()).max(axis=0)
        result = np.zeros(matrix_dimensions, dtype=int)
        for (i, j), count in result_dict.items():
            result[i, j] = count

        return result

    @property
    def weakly_directed_out_size_distribution(self):
        """Return a matrix of size distributions (per node) where
        the (i, j)th entry is the number of nodes with i edges of
        out size (number of elements weakly above) j incident on
        the node.

        Returns
        -------

        dist_matrix : numpy ndarray
            The size distribution matrix
        """
        result_dict = defaultdict(int)
        for node in self.nodes:
            for e in self.node[node]:
                for node_index in range(self.edge[e].multiplicity(node)):
                    sizes = Counter(len(self.edge[e].weakly_above(node, node_index)))
                    for i in sizes:
                        j = sizes[i]
                        result_dict[(i, j)] += 1

        matrix_dimensions = np.array(result_dict.keys()).max(axis=0)
        result = np.zeros(matrix_dimensions, dtype=int)
        for (i, j), count in result_dict.items():
            result[i, j] = count

        return result

    @property
    def weakly_directed_in_size_distribution(self):
        """Return a matrix of size distributions (per node) where
        the (i, j)th entry is the number of nodes with i edges of
        out size (number of elements weakly below) j incident on
        the node.

        Returns
        -------

        dist_matrix : numpy ndarray
            The size distribution matrix
        """
        result_dict = defaultdict(int)
        for node in self.nodes:
            for e in self.node[node]:
                for node_index in range(self.edge[e].multiplicity(node)):
                    sizes = Counter(len(self.edge[e].weakly_below(node, node_index)))
                    for i in sizes:
                        j = sizes[i]
                        result_dict[(i, j)] += 1

        matrix_dimensions = np.array(result_dict.keys()).max(axis=0)
        result = np.zeros(matrix_dimensions, dtype=int)
        for (i, j), count in result_dict.items():
            result[i, j] = count

        return result

    @property
    def strictly_directed_out_size_distribution(self):
        """Return a matrix of size distributions (per node) where
        the (i, j)th entry is the number of nodes with i edges of
        out size (number of elements strictly above) j incident on
        the node.

        Returns
        -------

        dist_matrix : numpy ndarray
            The size distribution matrix
        """
        result_dict = defaultdict(int)
        for node in self.nodes:
            for e in self.node[node]:
                for node_index in range(self.edge[e].multiplicity(node)):
                    sizes = Counter(len(self.edge[e].strictly_above(node, node_index)))
                    for i in sizes:
                        j = sizes[i]
                        result_dict[(i, j)] += 1

        matrix_dimensions = np.array(result_dict.keys()).max(axis=0)
        result = np.zeros(matrix_dimensions, dtype=int)
        for (i, j), count in result_dict.items():
            result[i, j] = count

        return result

    @property
    def strictly_directed_in_size_distribution(self):
        """Return a matrix of size distributions (per node) where
        the (i, j)th entry is the number of nodes with i edges of
        out size (number of elements strictly below) j incident on
        the node.

        Returns
        -------

        dist_matrix : numpy ndarray
            The size distribution matrix
        """
        result_dict = defaultdict(int)
        for node in self.nodes:
            for e in self.node[node]:
                for node_index in range(self.edge[e].multiplicity(node)):
                    sizes = Counter(len(self.edge[e].strictly_below(node, node_index)))
                    for i in sizes:
                        j = sizes[i]
                        result_dict[(i, j)] += 1

        matrix_dimensions = np.array(result_dict.keys()).max(axis=0)
        result = np.zeros(matrix_dimensions, dtype=int)
        for (i, j), count in result_dict.items():
            result[i, j] = count

        return result

    @property
    def networkx_flag_digraph(self):
        warn('Not implemented yet!')
        return None
