import pickle
from multiprocessing import Process, Queue, cpu_count

# worker function - gi hint na sa activity sheet ang structure
def worker(sub_data, target, q, offset):
    for i in range(len(sub_data)):
        if sub_data[i] == target:
            q.put(offset + i)  # ibalik ang global index
            return
    q.put(-1)  # wala makita sa this chunk

def parallel_search(data, target):
    n = cpu_count()
    chunk_size = len(data) // n
    q = Queue()
    processes = []

    # mag create ni siyag one process per chunk
    for i in range(n):
        start = i * chunk_size
        end = start + chunk_size if i < n - 1 else len(data)
        p = Process(target=worker, args=(data[start:end], target, q, start))
        processes.append(p)
        p.start()

    # hulatan sa niya mahuman ang tanan processes to finish
    for p in processes:
        p.join()

    # collect and resolve results from all processes
    results = [q.get() for _ in processes]
    found = [r for r in results if r != -1]
    return min(found) if found else -1  # return smallest index or -1

def choose_dataset():
    options = {
        "1": "small_random.pkl",
        "2": "medium_random.pkl",
        "3": "large_random.pkl",
        "4": "small_sorted.pkl",
        "5": "medium_sorted.pkl",
        "6": "large_sorted.pkl",
    }

    print("Choose a dataset:")
    print("1. small_random.pkl")
    print("2. medium_random.pkl")
    print("3. large_random.pkl")
    print("4. small_sorted.pkl")
    print("5. medium_sorted.pkl")
    print("6. large_sorted.pkl")
    print("Press Enter for default: small_random.pkl")

    choice = input("Enter choice (1-6): ").strip()
    return options.get(choice, "small_random.pkl")


if __name__ == "__main__":
    filename = choose_dataset()

    with open(f"datasets/{filename}", "rb") as f:
        data = pickle.load(f)

    target = 437287

    result = parallel_search(data, target)

    if result != -1:
        print(f"Found {target} at index {result}")
    else:
        print(f"{target} not found")