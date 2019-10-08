from splay_tree import SplayTree
import pytest


def test_insert():
    splay_tree = SplayTree()

    splay_tree.insert(10)
    splay_tree.insert(8)
    splay_tree.insert(12)
    splay_tree.insert(13)
    splay_tree.insert(7)

    x = splay_tree.pre_order(splay_tree.root(), [])

    assert x == [7, 8, 10, 12, 13]


def test_find():
    splay_tree = SplayTree()
    assert pytest.raises(ValueError, splay_tree.find, 1)

    splay_tree.insert(10, 10)
    splay_tree.insert(8, 8)
    splay_tree.insert(12, 12)

    assert splay_tree.find(8) == 8
    assert splay_tree.find(20) is None


def test_delete():
    splay_tree = SplayTree()
    splay_tree.insert(10)
    splay_tree.insert(8)
    splay_tree.insert(12)
    splay_tree.insert(13)
    splay_tree.insert(7)

    splay_tree.delete(12)
    x = splay_tree.pre_order(splay_tree.root(), [])
    assert x == [7, 8, 10, 13]

    splay_tree.delete(12)

    assert x == [7, 8, 10, 13]
