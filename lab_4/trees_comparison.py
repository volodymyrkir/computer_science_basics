import itertools
import sys
import timeit
import random

import pandas as pd

from weak_avl_tree import WAVLTree
from bst_tree import BST


def time_operation(tree, func, keys):
    operation_keys = random.sample(keys, keys // 5)
    for key in keys:
        tree.insert(key)
    start_time = timeit.default_timer()

    if func == 'delete':
        for key in operation_keys:
            tree.delete(key)
    elif func == 'search':
        for key in operation_keys:
            tree.search(key)
    elif func == 'successor':
        for key in operation_keys:
            tree.successor(key)
    elif func == 'predecessor':
        for key in operation_keys:
            tree.predecessor(key)
    end_time = timeit.default_timer()
    return end_time - start_time


def insert_and_capture_time(tree, inputs):
    start_time = timeit.default_timer()
    for key in inputs:
        tree.insert(key)
    return timeit.default_timer() - start_time


if __name__ == '__main__':
    input_sizes = [100, 500, 1000, 1500]
    sys.setrecursionlimit(1600)
    operations = ['delete', 'search', 'successor', 'predecessor']

    results = []
    for input_size, input_linear in itertools.product(input_sizes, [True, False]):
        keys = (
            [random.randint(1, input_size) for _ in range(input_size)]
            if input_linear else [i for i in range(input_size)]
        )
        wavl_insert = insert_and_capture_time(WAVLTree(), keys)
        bst_insert = insert_and_capture_time(BST(), keys)
        quickest_insert = 'WAVL' if wavl_insert < bst_insert else 'BST'
        results.append(['Insert', input_size, input_linear, wavl_insert, bst_insert, quickest_insert])
        for operation in operations:
            wavl_operation = insert_and_capture_time(WAVLTree(), keys)
            bst_operation = insert_and_capture_time(BST(), keys)
            quickest = 'WAVL' if wavl_operation < bst_operation else 'BST'
            results.append([operation, input_size, input_linear, wavl_operation, bst_operation, quickest])

    df = pd.DataFrame(results, columns=[
        'Operation', 'Input Size', 'Is linear?', 'WAVL Tree Time', 'BST Time', 'Quickest'
    ])
    print(df)
