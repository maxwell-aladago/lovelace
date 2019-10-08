"""
Author: Maxwell Aladago
Date: 09/27/2019
"""
from math import log2


class BinomialHeap:
    """
    Implements a binomial heap

    Properties
    ----------
    min_root: Node, a pointer to the smallest the node with the smallest key
    num_nodes: the number of elements in the heap
    """

    def __init__(self):
        self._min_root = None
        self._num_nodes = 0

    def find_min(self):
        return self._min_root

    def insert(self, new_node):
        """
        inserts a new node into the heap

        Arguments
        --------
        new_node: the node to add to the heap

        """
        if not isinstance(new_node, Node):
            raise ValueError("Error: insert requires a node. ")

        new_node.parent = None
        if self._min_root:
            self._link_nodes(self._min_root, new_node)
        else:
            self._min_root = new_node
            self._min_root.right_sibling = new_node
            self._min_root.left_sibling = new_node

        if self._min_root > new_node:
            self._min_root = new_node

        self._num_nodes += 1

    def merge(self, other):
        """
        merges a binomial heap with the this heap.

        Arguments
        ----------
        other: a pointer to a binomial heap or a node (indicating the linking point)
               If 'other' is a binomial heap, the new heap has as many elements as the
               sum of the elements in the this heap and 'other'. If `other' is a pointer to a node,
               it's assumed it's a heap rooted at at a root of this heap which is being promoted
        """
        min_root1 = self._min_root
        if isinstance(other, BinomialHeap):
            min_root2 = other.find_min()
            self._num_nodes += other.num_elements()
        elif isinstance(other, Node):
            min_root2 = other
        else:
            raise ValueError("Error: merge requires a pointer to a binomial heap or a node")

        min_root1.right_sibling.left_sibling = min_root2.left_sibling
        min_root2.left_sibling.right_sibling = min_root1.right_sibling
        min_root1.right_sibling = min_root2
        min_root2.left_sibling = min_root1

        if min_root1 > min_root2:
            self._min_root = min_root2

    def decrease_key(self, node, new_key):
        """
        decreases the key of a node given a pointer to the node

        Arguments
        ---------
        node: a pointer to node whose key is to be reduced
        new_key: the new key
        """
        if not isinstance(node, Node):
            raise ValueError("Error: decrease key requires a pointer to the target node.")
        if node.key < new_key:
            raise ValueError("Error: new key must be smaller than the old key")

        node.key = new_key
        parent = node.parent
        while parent is not None and parent > node:
            node.key = parent.key
            node.data = parent.data
            node = parent
            parent = node.parent

        if self._min_root > node:
            self._min_root = node

    def delete_min(self):
        """
        deletes the minimum node (highest priority) node from the heap.
        Resets the min_node pointer to the next smallest node and also
        merges trees of the same degrees.

        Returns
        -------
        min_root: the deleted node (the previous minimum)
        """
        if not self._min_root:
            raise ValueError("Error: no deletion can be made on an empty heap!")

        min_root = self._min_root
        if min_root.child is not None:
            self.merge(min_root.child)

        A = self._merge_trees_in_root_list()
        new_min_root = self._stick_nodes_to_make_heap(A)
        self._min_root = new_min_root

        self._num_nodes -= 1
        return min_root

    @staticmethod
    def make_heap():
        """
        Returns a new empty heap
        """
        return BinomialHeap()

    def delete(self, node):
        """
        Deletes a given node from the heap given a pointer to the node.
        """
        self.decrease_key(node, float("-inf"))
        self.delete_min()

    def num_elements(self):
        return self._num_nodes

    def _merge_trees_in_root_list(self):
        """
        A utility method which merges all trees in the heap of the same degree after a deletion

        Returns
        ------
        A: an array of pointers to the roots of the binomial trees which comprise the new heap.
        """
        A = [None] * int(log2(self._num_nodes) + 1)
        current = self._min_root.right_sibling
        while current != self._min_root:
            t = current
            current = current.right_sibling
            j = t.degree
            while A[j] is not None:
                t = self._merge_into_tree(t, A[j])
                A[j] = None
                j += 1
            A[j] = t
        return A

    @staticmethod
    def _stick_nodes_to_make_heap(A):
        """
        A utility method which links the roots of a binomial heap represented pointers in A

        Arguments
        ---------
         A: an array which holds pointers to a binomial trees comprising a binomial heap.

        Returns
        ------
        min_root: a pointer to the minimum root in A

        """
        min_root = A[0]
        prev = A[0]
        first = A[0]
        for i in range(1, len(A)):
            if A[i] is None:
                continue
            current = A[i]
            current.parent = None

            if min_root is None:
                min_root = current
                first = current
            else:
                prev.right_sibling = current
                current.left_sibling = prev
                if min_root > current:
                    min_root = current

            prev = current

        if first is not None:
            first.left_sibling = prev
            prev.right_sibling = first

        return min_root

    @staticmethod
    def _link_nodes(node1, node2):
        """
        A utility method which inserts node2 into the sibling list of node1 such that `node1` is on the left of `node2`
        """
        node2.right_sibling = node1.right_sibling
        node2.left_sibling = node1
        node1.right_sibling.left_sibling = node2
        node1.right_sibling = node2

    def _merge_into_tree(self, root1, root2):
        """
         A utility method which merges two binomial trees into one given pointers to their roots.

         Returns
         ------
            root1: a pointer to the root of the new tree (which is the smallest of the
                    two roots passed in).

        """
        if root1.degree != root2.degree:
            raise ValueError("Error: Merge expects the two roots to have the same degree."
                             "Found roots of different degrees")
        if root1 > root2:
            tempt = root1
            root1 = root2
            root2 = tempt

        if root1.child is not None:
            self._link_nodes(root1.child, root2)
        else:
            root2.right_sibling = root2
            root2.left_sibling = root2

        root2.parent = root1
        root1.child = root2
        root1.degree += 1

        return root1


class Node:
    """
    Model's a single node in the binomial heap.

    Properties:
    key: an object which implements all the comparable interfaces
         representing the priority of a node
    data: any object which holds any satellite data of the node
    parent: a pointer to the node's parent if any
    child: a pointer to the node's child if any
    right_sibling: a pointer to the node's right sibling if any
    left_sibling: a pointer to the node's left sibling if any
    degree: int, represents the degree of the node

    Note: All properties of a node can be reset after instantiation.
    """

    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.parent = None
        self.right_sibling = None
        self.left_sibling = None
        self.degree = 0
        self.child = None
        self.marked = False

    def __eq__(self, other):
        return Node._nodes_equal(self, other) and \
               Node._nodes_equal(self.left_sibling, other.left_sibling) and \
               Node._nodes_equal(self.right_sibling, other.right_sibling)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.key > other.key

    def __lt__(self, other):
        return self.key < other.key

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not self > other

    def __str__(self):
        return "(key={}, data={})".format(self.key, self.degree)

    @staticmethod
    def _nodes_equal(node1, node2):
        """
        utility method: returns True if and only if `node1` and 'node2' are
        equal or they are both null. Returns false otherwise
        """
        if node1 is None and node2 is None:
            return True
        return (node1 is not None and node2 is not None) and \
               (node1.key == node2.key) and (node1.data == node2.data)
