import math

from typing import Callable
from time import time

import pandas as pd
from matplotlib import pyplot as plt

from lab_2.utils import generate_array, measure_time
from logger import logger

ARRAY_LENGTHS = (10_000, 30_000, 90_000, 270_000, 810_000)
ARRAY_LENGTHS_TEST = (10_000, 20_000, 30_000)

VARIANT = 7

COMB_SORT_SHRINK = 1.247

EPSILON = 1e-9


@measure_time
def bubble_sort(array: list, array_len: int) -> list:
    start_time = time()
    for i in range(array_len - 1):
        for j in range(array_len - i - 1):
            if time() - start_time > 600:
                logger.info(f'Bubble sort execution is > 10 minutes')
                return array
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


@measure_time
def comb_sort(array: list, array_len: int) -> list:
    step = array_len
    is_sorted = False
    while not is_sorted:
        if step > 1:
            step = int(step / COMB_SORT_SHRINK)

        is_sorted = True

        for i in range(0, array_len - step):
            if array[i] > array[i + step]:
                array[i], array[i + step] = array[i + step], array[i]
                is_sorted = False

    return array


@measure_time
def radix_sort(array: list, array_len: int) -> list:
    def counting_sort_for_radix(array_inner: list, exp: int, array_len_inner: int = array_len):
        output = [0] * array_len_inner
        count = [0] * VARIANT

        for i in range(array_len_inner):
            index = (array_inner[i] // exp) % VARIANT
            count[index] += 1

        for i in range(1, VARIANT):
            count[i] += count[i - 1]

        for i in range(array_len_inner - 1, -1, -1):
            index = (array_inner[i] // exp) % VARIANT
            output[count[index] - 1] = array_inner[i]
            count[index] -= 1

        for i in range(array_len_inner):
            array_inner[i] = output[i]

    max_val = max(array)
    factor = 1
    while max_val // factor > 0:
        counting_sort_for_radix(array, factor)
        factor *= VARIANT

    return array


if __name__ == '__main__':
    functions_mapping = {'bubble_sort': bubble_sort, 'comb_sort': comb_sort, 'radix_sort': radix_sort}
    results = {'bubble_sort': [], 'comb_sort': [], 'radix_sort': []}

    for length in ARRAY_LENGTHS:
        arr = generate_array(length)

        for func_name, sort in functions_mapping.items():
            res = sort(arr, length)
            results[func_name].append(res['time'])

    df = pd.DataFrame({
        'lengths': ARRAY_LENGTHS,
        'Bubble Sort (s)': results['bubble_sort'],
        'Comb Sort (s)': results['comb_sort'],
        'Radix Sort (s)': results['radix_sort'],
    })
    logger.info(df)
    plt.figure(figsize=(10, 6))
    for method, times in results.items():
        log_lengths = [math.log10(x) for x in ARRAY_LENGTHS]
        log_times = [math.log10(y + EPSILON) for y in times]
        plt.plot(log_lengths, log_times, label=method)

    plt.xlabel('log(Array Length)')
    plt.ylabel('log(Time (s))')
    plt.title('Sorting Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()
