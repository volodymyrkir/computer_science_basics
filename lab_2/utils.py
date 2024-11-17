import random
from time import time
from typing import Callable

from logger import logger

VARIANT = 7
KEY = 10 * VARIANT

MIN_INT_VALUE, MAX_INT_VALUE = 0, 65535


def generate_array(
        num_elements: int,
        min_element: int = MIN_INT_VALUE,
        max_element: int = MAX_INT_VALUE,
        print_array: bool = True
) -> list:
    values = []
    for _ in range(num_elements):
        value = random.randint(min_element, max_element)
        while value == KEY:
            value = random.randint(min_element, max_element)
        values.append(value)
    logger.info(f'Generated a {len(values)}-length array.')
    if print_array:
        logger.info(f'Some of the elements: ...{random.sample(values, 10)}...')

    return values


def measure_time(func: Callable):
    def wrapper(*args, **kwargs):
        start = time()
        value = func(*args, **kwargs)
        end = time()
        return {'time': end - start, 'value': value}

    return wrapper
