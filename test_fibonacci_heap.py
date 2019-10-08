from fibonacci_heap import FibonacciHeap, Node
import pytest


def test_decrease_key():
    node1 = Node(34)
    node2 = Node(10)
    node3 = Node(12)
    node4 = Node(20)

    heap = FibonacciHeap()
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
    print(heap.find_min(), node3)
    assert heap.find_min().key == 8
