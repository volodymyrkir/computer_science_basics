from typing import Hashable, Any

from logger import logger

M = 31
PI = 3.1415

STUDENTS = [
    "Бражненко",
    "Величко",
    "Гробовий",
    "Гуков",
    "Жук",
    "Кізіченко",
    "Кірюшин",
    "Махотіло",
    "Мічурін",
    "Недодаєв",
    "Падалкін",
    "Пестун",
    "Селін",
    "Сторчай",
    "Стрельцов",
    "Шевченко"
]


class HashTable:
    def __init__(self, m: int = M):
        self._m = m
        self.table = [None] * m

    def _calculate_hash(self, key: str) -> int:
        sum_hash = 0
        for char in key:
            sum_hash += int(ord(char) * PI)
        return sum_hash % self._m

    def put(self, key: str, value: Any) -> tuple[int, int, Any]:
        index = self._calculate_hash(key)

        original_index = index
        steps = 0

        while self.table[index] is not None and self.table[index][0] != key:
            index = (index + 1) % self._m
            steps += 1
            if index == original_index:
                raise Exception("HashTable is full!")

        self.table[index] = (key, value)
        logger.info(f"Inserted key {key} at index {index} (steps taken: {steps})")
        return original_index, index, steps

    def search(self, key: str) -> Any:
        index = self._calculate_hash(key)
        original_index = index
        steps = 0

        while self.table[index] is not None:
            if self.table[index][0] == key:
                logger.info(f"Key {key} found at index {index} (steps taken: {steps})")
                return self.table[index][1]
            index = (index + 1) % self._m
            steps += 1
            if index == original_index:
                break

        logger.info(f"Key {key} not found (steps taken: {steps})")

    def display(self) -> None:
        logger.info("Hash Table:")
        for i, entry in enumerate(self.table):
            logger.info(f"Index {i}: {entry}")


if __name__ == "__main__":

    hash_table = HashTable()

    results = {
        'Номер за списком': [],
        'Прізвище': [],
        'Первинне значення хеш-функції («рідний» індекс у хеш-таблиці)': [],
        'Остаточне значення хешфункції (фактичний індекс у хеш-таблиці)': [],
        'Кількість колізій під час вставки': []
    }

    for value, key in enumerate(STUDENTS, start=1):
        primary_index, final_index, collisions = hash_table.put(key, value)
        results['Номер за списком'].append(value)
        results['Прізвище'].append(key)
        results['Первинне значення хеш-функції («рідний» індекс у хеш-таблиці)'].append(primary_index)
        results['Остаточне значення хешфункції (фактичний індекс у хеш-таблиці)'].append(final_index)
        results['Кількість колізій під час вставки'].append(collisions)

    header = f"{'Номер за списком':^20} | {'Прізвище':^20} | {'Первинне значення':^17} | {'Остаточне значення':^18} | {'Кількість колізій':^20}"
    logger.info("=" * len(header))
    logger.info(header)
    logger.info("=" * len(header))

    for i in range(len(results['Номер за списком'])):
        row = (f"{results['Номер за списком'][i]:^20} "
               f"| {results['Прізвище'][i]:^20} "
               f"| {results['Первинне значення хеш-функції («рідний» індекс у хеш-таблиці)'][i]:^17} "
               f"| {results['Остаточне значення хешфункції (фактичний індекс у хеш-таблиці)'][i]:^18} "
               f"| {results['Кількість колізій під час вставки'][i]:^20}")
        logger.info(row)

    logger.info("=" * len(header))

    hash_table.search("Мічурін")
    hash_table.search("Гуков")
    hash_table.search("Student")  # Non-existing key
