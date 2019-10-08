from binomial_heap import BinomialHeap, Node


def test_inserts(max_number):
    heap = BinomialHeap()

    for i in range(max_number):
        node = Node(i)
        heap.insert(node)

    return heap


def test_delete_mins(heap, max_deletions):
    max_deletions = min(heap.num_elements(), max_deletions)
    for i in range(max_deletions):
        heap.delete_min()


def test_insertions_deletions(max_iterations):
    heap = BinomialHeap()

    for i in range(max_iterations):
        heap.insert(Node(i))
        if i % 5 == 0:
            heap.delete_min()


def test_mix_operations(max_iterations):
    heap = BinomialHeap()
    for i in range(1, max_iterations):
        node = Node(i)
        heap.insert(node)
        heap.find_min()

        if i % 5 == 0:
            heap.decrease_key(prev, prev.key - 2)

        if i % 3 == 0:
            heap.delete_min()
            prev = heap.find_min()


def test_find_mins(max_iteration):
    heap = BinomialHeap()
    heap.insert(Node(1))

    for i in range(max_iteration):
        heap.find_min()


iterations = 2000000
heap = test_inserts(iterations)


def main():
    import timeit
    print("find_mins: {} seconds".format(timeit.timeit("test_find_mins(iterations)",
                                                       globals=globals(), number=1)))
    print("inserts: {} seconds".format(timeit.timeit("test_inserts(iterations)",
                                                     globals=globals(), number=1)))
    print("delete_mins: {} seconds".format(timeit.timeit("test_delete_mins(heap, iterations)",
                                                         globals=globals(), number=1)))
    print("insertions_deletions: {} seconds".format(timeit.timeit("test_insertions_deletions(iterations)",
                                                                  globals=globals(), number=1)))
    print("Mix-operation: {} seconds".format(timeit.timeit("test_mix_operations(iterations)",
                                                           globals=globals(), number=1)))


if __name__ == '__main__':
    main()
