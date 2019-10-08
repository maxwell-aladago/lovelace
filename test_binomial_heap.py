from binomial_heap import BinomialHeap, Node

import pytest


def test_make_heap():
    heap = BinomialHeap.make_heap()
    assert isinstance(heap, BinomialHeap)


def test_insert():
    heap = BinomialHeap()
    assert heap.num_elements() == 0

    new_node1 = Node(2)
    heap.insert(new_node1)

    assert heap.num_elements() == 1
    assert new_node1.right_sibling == new_node1
    assert new_node1.right_sibling == new_node1

    new_node2 = Node(3)
    heap.insert(new_node2)
    assert heap.num_elements() == 2

    assert new_node1.right_sibling == new_node2
    assert new_node1.left_sibling == new_node2
    assert new_node2.right_sibling == new_node1
    assert new_node2.left_sibling == new_node1

    # min_root now new node3 = 1
    new_node3 = Node(1)
    heap.insert(new_node3)
    assert heap.num_elements() == 3

    assert new_node3.right_sibling == new_node2
    assert new_node3.left_sibling == new_node1
    assert new_node3.right_sibling == new_node2
    assert new_node2.left_sibling == new_node3
    assert new_node1.right_sibling == new_node3
    assert new_node1.left_sibling == new_node2


def test_find_min():
    heap = BinomialHeap()
    assert heap.find_min() is None

    # min_root  new_node1 = 2
    new_node1 = Node(2)
    heap.insert(new_node1)
    min_root = heap.find_min()
    assert new_node1 == min_root

    new_node2 = Node(3)
    heap.insert(new_node2)
    min_root = heap.find_min()

    # min_root still new_node1 = 2
    assert min_root == new_node1

    new_node3 = Node(1)
    heap.insert(new_node3)
    min_root = heap.find_min()

    # min_root now new node3 = 1
    assert min_root == new_node3


def test_decrease_key():
    node1 = Node(34)
    node2 = Node(10)
    node3 = Node(12)
    node4 = Node(20)

    heap = BinomialHeap()
    heap.insert(node1)
    heap.insert(node2)
    heap.insert(node3)
    heap.insert(node4)

    assert heap.num_elements() == 4
    assert heap.find_min() == node2
    pytest.raises(ValueError, heap.decrease_key, node3, 13)
    pytest.raises(ValueError, heap.decrease_key, None, 13)
    heap.decrease_key(node3, 11)
    assert node3.key == 11
    assert heap.find_min() == node2

    heap.decrease_key(node3, 8)
    assert heap.find_min() == node3
    assert heap.find_min().key == 8


def test_delete_min():
    node1 = Node(34)
    node2 = Node(10)
    node3 = Node(12)
    node4 = Node(20)

    heap = BinomialHeap()
    heap.insert(node1)
    heap.insert(node2)
    heap.insert(node3)
    heap.insert(node4)

    assert heap.find_min() == node2
    assert heap.num_elements() == 4

    assert heap.delete_min() == node2
    assert heap.find_min() == node3
    assert heap.num_elements() == 3

    assert heap.delete_min() == node3
    assert heap.num_elements() == 2

    assert heap.find_min() == node4
    assert heap.delete_min() == node4

    assert heap.find_min() == node1
    assert heap.delete_min() == node1

    assert heap.find_min() is None
    assert heap.num_elements() == 0


def test_merge():
    node1 = Node(34)
    node2 = Node(10)
    node3 = Node(12)
    node4 = Node(20)

    heap1 = BinomialHeap()
    heap1.insert(node1)
    heap1.insert(node2)
    heap1.insert(node3)
    heap1.insert(node4)

    assert heap1.find_min() == node2
    assert heap1.num_elements() == 4

    node5 = Node(3)
    node6 = Node(11)
    node7 = Node(14)
    node8 = Node(20)

    heap2 = BinomialHeap()
    heap2.insert(node5)
    heap2.insert(node6)
    heap2.insert(node7)
    heap2.insert(node8)

    assert heap2.find_min() == node5

    heap1.merge(heap2)
    assert heap1.find_min() == node5
    assert heap1.num_elements() == 8

    b = heap1.delete_min()
    assert b == node5
    assert heap1.find_min() == node2


