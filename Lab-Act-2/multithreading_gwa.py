#Multithreading GWA Calculator

import threading
import time
from typing import List, Tuple

results_lock = threading.Lock()
results = []


def compute_gwa(subject_name: str, grade: float, thread_id: int) -> None:
    time.sleep(0.01)
    with results_lock:
        results.append((subject_name, grade))
        print(f"[Thread-{thread_id}] Processed {subject_name}: {grade}")


def calculate_final_gwa(grades: List[float]) -> float:
    if not grades:
        return 0.0
    return sum(grades) / len(grades)


def run_multithreading_gwa() -> Tuple[float, float]:
    global results
    results = []
    
    print("\n" + "="*60)
    print("GRADE COMPUTING SYSTEM - MULTITHREADING")
    print("="*60)
    
    # Get number of subjects
    while True:
        try:
            num_subjects = int(input("\nEnter number of subjects: "))
            if num_subjects > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Collect subject names and grades
    subjects_data = []
    for i in range(num_subjects):
        subject_name = input(f"Enter subject {i+1} name: ")
        while True:
            try:
                grade = float(input(f"Enter grade for {subject_name} (0-100): "))
                if 0 <= grade <= 100:
                    subjects_data.append((subject_name, grade))
                    break
                print("Grade must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    print("\n" + "-"*60)
    print("Processing grades using MULTITHREADING...")
    print("-"*60)
    
    # Start timing
    start_time = time.time()
    
    # Create and start threads
    threads = []
    for idx, (subject, grade) in enumerate(subjects_data):
        t = threading.Thread(
            target=compute_gwa,
            args=(subject, grade, idx + 1)
        )
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    # Calculate GWA
    grades_only = [grade for _, grade in results]
    gwa = calculate_final_gwa(grades_only)
    
    # End timing
    execution_time = time.time() - start_time
    
    # Display results
    print("\n" + "-"*60)
    print("RESULTS")
    print("-"*60)
    for subject, grade in results:
        print(f"{subject:.<30} {grade:.2f}")
    print("-"*60)
    print(f"GENERAL WEIGHTED AVERAGE (GWA): {gwa:.2f}")
    print(f"Execution Time: {execution_time:.6f} seconds")
    print("="*60)
    
    return gwa, execution_time


if __name__ == "__main__":
    run_multithreading_gwa()
