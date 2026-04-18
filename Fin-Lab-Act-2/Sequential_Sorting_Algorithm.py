import os
import pickle
import sys


DATASET_DIR = os.path.join(os.path.dirname(__file__), "datasets")
DATASETS = [
	"small_random.pkl",
	"medium_random.pkl",
	"large_random.pkl",
	"small_sorted.pkl",
	"medium_sorted.pkl",
	"large_sorted.pkl",
]


# Recursive quicksort for sequential sorting.
def quicksort(data):
	if len(data) <= 1:
		return data

	# Split values around a pivot, then recursively sort each side.
	pivot = data[len(data) // 2]
	left = [x for x in data if x < pivot]
	middle = [x for x in data if x == pivot]
	right = [x for x in data if x > pivot]
	return quicksort(left) + middle + quicksort(right)


# Quick output check for report/demo readability.
def validate_first_last_five(sorted_data):
	first_five = sorted_data[:5]
	last_five = sorted_data[-5:]
	is_sorted = all(sorted_data[i] <= sorted_data[i + 1] for i in range(len(sorted_data) - 1))

	print(f"First 5: {first_five}")
	print(f"Last 5:  {last_five}")
	print(f"Sorted Correctly: {is_sorted}")


# Load one dataset list from the local datasets folder.
def load_dataset(filename):
	path = os.path.join(DATASET_DIR, filename)
	with open(path, "rb") as file:
		return pickle.load(file)


# Run sequential quicksort on one selected dataset.
def run_sequential_sort(filename="small_random.pkl"):
	data = load_dataset(filename)
	sorted_data = quicksort(data)

	print(f"Dataset: {filename}")
	print(f"Elements: {len(data)}")
	validate_first_last_five(sorted_data)

	return sorted_data


# Interactive picker when no command-line argument is provided.
def choose_dataset():
	print("Choose a dataset:")
	for i, name in enumerate(DATASETS, start=1):
		print(f"{i}. {name}")
	print("Press Enter for default: small_random.pkl")

	choice = input("Enter choice (1-6): ").strip()
	if choice.isdigit():
		index = int(choice) - 1
		if 0 <= index < len(DATASETS):
			return DATASETS[index]
	return "small_random.pkl"


# Parse CLI input so the script can run in automatic test mode.
def parse_dataset_argument(args):
	if not args:
		return None

	# Accept either dataset index (1-6) or exact filename.
	arg = args[0].strip()
	if arg.isdigit():
		index = int(arg) - 1
		if 0 <= index < len(DATASETS):
			return DATASETS[index]
	if arg in DATASETS:
		return arg
	return None


if __name__ == "__main__":
	# Prefer CLI dataset selection; otherwise ask interactively.
	selected_dataset = parse_dataset_argument(sys.argv[1:])
	if selected_dataset is None:
		selected_dataset = choose_dataset()
	run_sequential_sort(selected_dataset)
