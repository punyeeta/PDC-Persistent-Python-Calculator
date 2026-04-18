import importlib.util
import os
import sys
import time


BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SEQUENTIAL_FILE = os.path.join(PROJECT_ROOT, "Sequential_Sorting_Algorithm.py")
PARALLEL_FILE = os.path.join(PROJECT_ROOT, "Parallel_Sorting_Algorithm.py")
DATASETS = [
    "small_random.pkl",
    "medium_random.pkl",
    "large_random.pkl",
    "small_sorted.pkl",
]

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def load_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def evaluate_sequential_sort(seq_module):
    print("\n=== Sequential Quicksort Evaluation ===")
    for dataset in DATASETS:
        try:
            start = time.time()
            seq_module.run_sequential_sort(dataset)
            runtime = time.time() - start
            print(f"Summary -> {dataset}: {runtime:.6f} seconds\n")
        except FileNotFoundError:
            print(f"Skipped {dataset}: dataset file not found.\n")


def evaluate_python_sorted(seq_module):
    print("\n=== Python built-in sorted() Baseline ===")
    for dataset in DATASETS:
        try:
            data = seq_module.load_dataset(dataset)
            start = time.time()
            output = sorted(data)
            end = time.time()

            print(f"Dataset: {dataset}")
            print(f"Elements: {len(data)}")
            print(f"Execution Time: {end - start:.6f} seconds")
            seq_module.validate_first_last_five(output)
            print()
        except FileNotFoundError:
            print(f"Skipped {dataset}: dataset file not found.\n")


def evaluate_parallel_sort(par_module):
    print("\n=== Parallel Quicksort Evaluation ===")
    for dataset in DATASETS:
        try:
            start = time.time()
            par_module.run_parallel_sort(dataset)
            runtime = time.time() - start
            print(f"Summary -> {dataset}: {runtime:.6f} seconds\n")
        except FileNotFoundError:
            print(f"Skipped {dataset}: dataset file not found.\n")


def main():
    seq_module = load_module_from_file("Sequential_Sorting_Algorithm", SEQUENTIAL_FILE)
    par_module = load_module_from_file("Parallel_Sorting_Algorithm", PARALLEL_FILE)

    evaluate_sequential_sort(seq_module)
    evaluate_parallel_sort(par_module)
    evaluate_python_sorted(seq_module)


if __name__ == "__main__":
    main()
