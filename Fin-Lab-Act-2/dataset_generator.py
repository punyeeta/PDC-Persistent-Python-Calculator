import os
import pickle
import random

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "datasets")
DATASET_SIZES = {
    "small": 1_000,
    "medium": 100_000,
    "large": 1_000_000,
}

def save(name, data):
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, "wb") as file:
        pickle.dump(data, file)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for label, N in DATASET_SIZES.items():
       
        data = [random.randint(1, 1_000_000) for _ in range(N)]
        save(f"{label}_random.pkl", data)
        save(f"{label}_sorted.pkl", sorted(data))

    print("Done. Datasets saved in:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
