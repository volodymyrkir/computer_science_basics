import random
import time
from typing import Callable

import pandas as pd

from lab_2.utils import KEY, generate_array, measure_time
from logger import logger

ARRAY_SIZES = [100, 1_000, 10_000, 100_000]
MIN_VALUE = -65535
ITERATIONS = 100


def measure_time_inserts(func: Callable):
    def wrapper(*args, **kwargs):
        total_time = 0
        for _ in range(ITERATIONS):
            start = time.perf_counter()
            value = func(*args, **kwargs)
            total_time += time.perf_counter() - start
        return {'time': total_time / ITERATIONS, 'value': value}

    return wrapper


def prepare_array(size: int):
    array = generate_array(size, min_element=MIN_VALUE)
    array[random.randint(0, size - 1)] = KEY
    sorted_array = sorted(array)
    logger.info(f'The position of key in the array is {sorted_array.index(KEY)}')
    return sorted_array


@measure_time_inserts
def binary_search(arr: list, key: int):
    low, high = 0, len(arr) - 1
    iterations, comparisons = 0, 0

    while low <= high:
        iterations += 1
        mid = (low + high) // 2
        comparisons += 1

        if arr[mid] == key:
            return mid, iterations, comparisons
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
        comparisons += 1

    return -1, iterations, comparisons


@measure_time_inserts
def interpolation_search(arr: list, key: int):
    low, high = 0, len(arr) - 1
    iterations, comparisons = 0, 0

    while low <= high and arr[low] <= key <= arr[high]:
        iterations += 1
        if low == high:
            comparisons += 1
            if arr[low] == key:
                return low, iterations, comparisons
            break

        pos = low + ((high - low) * (key - arr[low]) // (arr[high] - arr[low]))
        comparisons += 1

        if arr[pos] == key:
            return pos, iterations, comparisons
        if arr[pos] < key:
            low = pos + 1
        else:
            high = pos - 1
        comparisons += 1

    return -1, iterations, comparisons


def measure_average_search(search_func: Callable, array: list):
    metrics = {'time': [], 'iterations': [], 'comparisons': []}

    for key in array:
        res = search_func(array, key)
        (_, iterations, comparisons), time_took = res['value'], res['time']
        metrics['time'].append(time_took)
        metrics['iterations'].append(iterations)
        metrics['comparisons'].append(comparisons)

    avg_time = sum(metrics['time']) / len(metrics['time'])
    avg_iterations = sum(metrics['iterations']) / len(metrics['iterations'])
    avg_comparisons = sum(metrics['comparisons']) / len(metrics['comparisons'])

    return avg_time, avg_iterations, avg_comparisons


if __name__ == "__main__":
    results = []  # List to store all results

    for size in ARRAY_SIZES:
        array = prepare_array(size)

        # Measure average metrics for Binary Search
        bin_avg_time, bin_avg_iter, bin_avg_comp = measure_average_search(binary_search, array)
        bin_res = binary_search(array, KEY)
        (bin_pos, bin_iter, bin_comp), bin_time = bin_res['value'], bin_res['time']

        # Measure average metrics for Interpolation Search
        interp_avg_time, interp_avg_iter, interp_avg_comp = measure_average_search(interpolation_search, array)
        interp_res = interpolation_search(array, KEY)
        (interp_pos, interp_iter, interp_comp), interp_time = interp_res['value'], interp_res['time']

        # Ensure correctness
        assert all(found_pos == array.index(KEY) for found_pos in [bin_pos, interp_pos]), "Wrong search position"

        # Append Binary Search results to the list
        results.append({
            "array_size": size,
            "search_method": "Binary Search",
            "avg_time": bin_avg_time,
            "avg_iterations": bin_avg_iter,
            "avg_comparisons": bin_avg_comp,
            "find_key_time": bin_time,
            "find_key_iters": bin_iter,
            "find_key_comps": bin_comp,
            "key_position": bin_pos
        })

        # Append Interpolation Search results to the list
        results.append({
            "array_size": size,
            "search_method": "Interpolation Search",
            "avg_time": interp_avg_time,
            "avg_iterations": interp_avg_iter,
            "avg_comparisons": interp_avg_comp,
            "find_key_time": interp_time,
            "find_key_iters": interp_iter,
            "find_key_comps": interp_comp,
            "key_position": interp_pos
        })

    # Create a DataFrame from the results
    pd.set_option('display.max_columns', None)
    df_results = pd.DataFrame(results)

    # Save or print the DataFrame
    print(df_results)