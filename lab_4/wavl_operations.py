from weak_avl_tree import WAVLTree
import random


def run_experiment(tree, keys, num_operations=200_000):
    for key in keys:
        tree.insert(key)
    operation_types = ['insert', 'delete', 'search']
    results = {'insert': {'node_visits': 0, 'rotations': 0},
               'delete': {'node_visits': 0, 'rotations': 0},
               'search': {'node_visits': 0, 'rotations': 0}}

    for _ in range(num_operations):
        operation = random.choice(operation_types)
        op_key = random.choice(keys)
        tree.reset_metrics()

        if operation == 'insert':
            tree.insert(op_key)
            results['insert']['node_visits'] += tree.node_visit_count
            results['insert']['rotations'] += tree.rotation_count
        elif operation == 'delete':
            tree.delete(op_key)
            results['delete']['node_visits'] += tree.node_visit_count
            results['delete']['rotations'] += tree.rotation_count
        else:  # search
            tree.search(op_key)
            results['search']['node_visits'] += tree.node_visit_count
            results['search']['rotations'] += tree.rotation_count

    for op in results:
        results[op]['node_visits'] /= num_operations
        results[op]['rotations'] /= num_operations

    return results


if __name__ == "__main__":
    num_runs = 10
    all_results = {'insert': {'node_visits': 0, 'rotations': 0},
                   'delete': {'node_visits': 0, 'rotations': 0},
                   'search': {'node_visits': 0, 'rotations': 0}}

    for i in range(num_runs):
        print(f'Trial {i + 1}')
        tree = WAVLTree()
        keys = [random.randint(1, 1_000_000) for _ in range(1_000_000)]
        results = run_experiment(tree, keys)
        for op in results:
            all_results[op]['node_visits'] += results[op]['node_visits']
            all_results[op]['rotations'] += results[op]['rotations']

    for op in all_results:
        all_results[op]['node_visits'] /= num_runs
        all_results[op]['rotations'] /= num_runs

    print("Averaged results after 10 runs:")
    for op in all_results:
        print(f"{op.capitalize()} - Average Node Visits: {all_results[op]['node_visits']},"
              f" Average Rotations: {all_results[op]['rotations']}")
