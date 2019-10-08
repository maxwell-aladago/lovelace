from binomial_heap import BinomialHeap, Node


class FibonacciHeap(BinomialHeap):
    def __init__(self):
        super(BinomialHeap, self).__init__()

    def make_heap(self):
        return FibonacciHeap()

    def decrease_key(self, node, new_key):
        if not isinstance(node, Node):
            raise ValueError("Error: decrease key expects a pointer to a node. ")

        if node.key < new_key:
            raise ValueError("Error: new key must be strictly less than the current key!")

        node.key = new_key
        if node.parent and new_key < node.parent.key:
            node.marked = True

            while node.parent and node.marked:
                p = node.parent
                node.marked = False
                self._cut(node)
                self.insert(node)
                node = p
                node.degree -= node.degree

        if node.parent:
            node.marked = True
        elif node < self.find_min():
            self._min_root = node

    @staticmethod
    def _cut(node):
        left = node.left_sibling
        right = node.right_sibling
        left.right_sibling = right
        right.left_sibling = left
