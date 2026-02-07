#Mutliprocessing GWA Calculator

from multiprocessing import Process, Queue
import time
from typing import List, Tuple


def compute_gwa_mp(subject_name: str, grade: float, process_id: int, result_queue: Queue) -> None:
    # Simulate some processing time
    time.sleep(0.01)
    
    # Store result in queue (process-safe)
    result_queue.put((subject_name, grade))
    print(f"[Process-{process_id}] Processed {subject_name}: {grade}")


def calculate_final_gwa(grades: List[float]) -> float:
    if not grades:
        return 0.0
    return sum(grades) / len(grades)


def run_multiprocessing_gwa() -> Tuple[float, float]:
    print("\n" + "="*60)
    print("GRADE COMPUTING SYSTEM - MULTIPROCESSING")
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
    print("Processing grades using MULTIPROCESSING...")
    print("-"*60)
    
    # Create a queue for collecting results
    result_queue = Queue()
    
    # Start timing
    start_time = time.time()
    
    # Create and start processes
    processes = []
    for idx, (subject, grade) in enumerate(subjects_data):
        p = Process(
            target=compute_gwa_mp,
            args=(subject, grade, idx + 1, result_queue)
        )
        processes.append(p)
        p.start()
    
    # Wait for all processes to complete
    for p in processes:
        p.join()
    
    # Collect results from queue
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
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
    run_multiprocessing_gwa()
