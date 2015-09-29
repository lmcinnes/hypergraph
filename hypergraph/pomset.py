import numpy as np

def _order_bfs(order, direction='up'):
	if direction == 'up':
		
		pass
	elif direction == 'down':

		pass
	else:
		raise ValueError('bfs direction must be either "up" or "down"')

class POMSet (object):
	'''A Partially Ordered Multiset.

	A POMSet is composed of labels (the items in the multiset) and
	an order (the partial order of the labels). Partial orders are
	provided as 2 dimensional numpy ndarray specifying order relations
	on the `i`th and `j`th labels as 
		order[i,j] == 1  <==> labels[i] > label[j]
		order[i,j] == 0  <==> label[i] is unrelated to label[j]
		order[i,j] == -1 <==> label[i] < label[j]

	The `size` of a POMSet is the number of labels.
	The `support` of a POMSet is the set of distinct labels.
	The `cardinality` of a POMSet is the size of the support.
	'''

	def __init__(self, labels=None, order=None):

		if labels is not None:
			self.labels = np.array(labels, dtype=object)
		else:
			self.labels = np.array([], dtype=object)

		self.size = len(self.labels)
		self.support = set(self.labels)
		self.cardinality = len(self.support)

		if order is not None:
			assert(order.shape[0] == len(self.labels))
			self.order = order
		else:
			self.order = np.zeros((self.size, self.size), dtype=np.int8)

	def weakly_above(self, element, element_index=0):
		'''
		'''
		label_index = np.where(self.labels == element)[0][element_index]
		return self.labels[~(self.order[label_index] == -1)]

	def _indices_strictly_above(self, element, element_index=0):
		label_index = np.where(self.labels == element)[0][element_index]
		return np.where[(self.order[label_index] == 1)][0]

	def strictly_above(self, element, element_index=0):
		label_index = np.where(self.labels == element)[0][element_index]
		return self.labels[(self.order[label_index] == 1)]

	def weakly_below(self, element, element_index=0):
		label_index = np.where(self.labels == element)[0][element_index]
		return self.labels[~(self.order[label_index] == 1)]

	def _indices_strictly_below(self, element, element_index=0):
		label_index = np.where(self.labels == element)[0][element_index]
		return np.where[(self.order[label_index] == -1)]

	def strictly_below(self, element, element_index=0):
		label_index = np.where(self.labels == element)[0][element_index]
		return self.labels[(self.order[label_index] == -1)]

	def weakly_greater_than(self, element1, element2, element1_index=0, element2_index=0):
		label_index1 = np.where(self.labels == element1)[0][element_index1]
		label_index2 = np.where(self.labels == element2)[0][element_index2]
		return self.order[label_index1, label_index2] >= 0

	def strictly_greater_than(self, element1, element2, element1_index=0, element2_index=0):
		label_index1 = np.where(self.labels == element1)[0][element_index1]
		label_index2 = np.where(self.labels == element2)[0][element_index2]
		return self.order[label_index1, label_index2] > 0

	def weakly_less_than(self, element1, element2, element1_index=0, element2_index=0):
		label_index1 = np.where(self.labels == element1)[0][element_index1]
		label_index2 = np.where(self.labels == element2)[0][element_index2]
		return self.order[label_index1, label_index2] <= 0

	def strictly_less_than(self, element1, element2, element1_index=0, element2_index=0):
		label_index1 = np.where(self.labels == element1)[0][element_index1]
		label_index2 = np.where(self.labels == element2)[0][element_index2]
		return self.order[label_index1, label_index2] < 0

	def add_label(self, new_label):
		new_label_array = np.empty(self.size + 1, dtype=object)
		new_label_array[:-1] = self.labels
		del self.labels
		self.labels = new_label_array
		self.labels[-1] = new_label

		self.size = len(self.labels)
		self.support.add(new_label)
		self.cardinality = len(self.support)

		new_order = np.zeros((self.size, self.size), dtype=np.int8)
		new_order[:-1][:-1] = self.order
		del self.order
		self.order = new_order

	def add_dependency(self, from_label, to_label, from_index=0, to_index=0):
		from_label_index = np.where(self.labels == from_label)[0][from_index]
		to_label_index = np.where(self.labels == to_label)[0][to_index]

		self.order[from_label_index, to_label_index] = -1
		self.order[to_label_index, from_label_index] = 1

		self.order[from_label_index, self._indices_strictly_above(to_label, to_index)] = -1
		self.order[to_label_index, self._indices_strictly_below(from_label, from_index)] = 1
