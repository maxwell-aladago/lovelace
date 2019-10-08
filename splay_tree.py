class SplayTree:

    def __init__(self):
        self._root = None

    def root(self):
        return self._root

    def insert(self, k, data=None):
        node = SplayTree.Node(k, data)
        if not self._root:
            self._root = node
        else:
            self.__splay(k)
            if self._root.key < k:
                node.left = self._root
                node.right = self._root.right
            else:
                node.right = self._root
                node.left = self._root.left

            if node.right:
                node.right.parent = node
            if node.left:
                node.left.parent = node

            self._root = node

    def find(self, k):
        self.__splay(k)
        if self._root.key == k:
            return self._root.data
        else:
            return None

    def delete(self, k):
        self.__splay(k)
        root = self._root
        if root.key == k:
            if root.left and root.right:
                self._root = root.right
                self._root.parent = None
                self.__splay(float('-inf'))
                root.left.parent = self._root
                self._root.left = root.left
            elif root.left:
                self._root = root.left
            else:
                self._root = root.right

            self._root.parent = None

    def pre_order(self, x, nodes):
        if x is None:
            return nodes
        nodes = self.pre_order(x.left, nodes)
        nodes.append(x.key)
        nodes = self.pre_order(x.right, nodes)
        return nodes

    @staticmethod
    def __rotate(x):
        p = x.parent
        if p.left == x:
            p.left = x.right
            x.right = p
        else:
            p.right = x.left
            x.left = p

        if p.right:
            p.right.parent = p
        if p.left:
            p.left.parent = p

        if p.parent:
            if p.parent.left == p:
                p.parent.left = x
            else:
                p.parent.right = x

        x.parent = p.parent
        p.parent = x

    def __splay(self, k):

        if self._root is None:
            raise ValueError("Error: cannot execute operation on empty tree.")

        x = self._root
        p = None

        while x and x.key != k:
            p = x
            if k < x.key:
                x = x.left
            elif k > x.key:
                x = x.right
        if x is None:
            x = p

        while x.parent and x.parent.parent:
            p = x.parent
            g = p.parent

            if (x == p.left and p == g.left) or (x == p.right and p == g.right):
                self.__rotate(p)
                self.__rotate(x)
            else:
                self.__rotate(x)
                self.__rotate(x)

        if x.parent:
            self.__rotate(x)

        self._root = x

    class Node:
        def __init__(self, key, data=None):
            self.key = key
            self.data = data
            self.parent = None
            self.left = None
            self.right = None

        def __str__(self):
            return "(key={}, data={})".format(self.key, self.data)

        def __eq__(self, other):
            equal = (self is not None and other is not None) and\
                    (self.key == other.key and self.data == other.data)

            return equal

        def __lt__(self, other):
            return self.key < other.key

        def __gt__(self, other):
            return self.key > other.key

        def __ne__(self, other):
            return not self.__eq__(other)

        def __le__(self, other):
            return not self > other

        def __ge__(self, other):
            return not self < other
