#Test Computation and Comparison of Multithreading and Multiprocessing GWA Calculators

import threading
import time
from multiprocessing import Process, Queue
from typing import List, Tuple
import statistics


def compute_gwa_thread(subject_name: str, grade: float, thread_id: int, results: List, lock: threading.Lock) -> None:
    time.sleep(0.001)  # Small delay to simulate processing
    with lock:
        results.append((subject_name, grade))
        print(f"[Thread-{thread_id}] {subject_name}: {grade}")


def compute_gwa_process(subject_name: str, grade: float, process_id: int, result_queue: Queue) -> None:
    time.sleep(0.001)  # Small delay to simulate processing
    result_queue.put((subject_name, grade))
    print(f"[Process-{process_id}] {subject_name}: {grade}")


def test_multithreading(subjects_data: List[Tuple[str, float]]) -> Tuple[float, float, List[Tuple[str, float]]]:
    results = []
    results_lock = threading.Lock()
    
    start_time = time.time()
    
    threads = []
    for idx, (subject, grade) in enumerate(subjects_data):
        t = threading.Thread(
            target=compute_gwa_thread,
            args=(subject, grade, idx + 1, results, results_lock)
        )
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    execution_time = time.time() - start_time
    grades = [g for _, g in results]
    gwa = sum(grades) / len(grades) if grades else 0
    
    return gwa, execution_time, results


def test_multiprocessing(subjects_data: List[Tuple[str, float]]) -> Tuple[float, float, List[Tuple[str, float]]]:
    result_queue = Queue()
    
    start_time = time.time()
    
    processes = []
    for idx, (subject, grade) in enumerate(subjects_data):
        p = Process(
            target=compute_gwa_process,
            args=(subject, grade, idx + 1, result_queue)
        )
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    execution_time = time.time() - start_time
    grades = [g for _, g in results]
    gwa = sum(grades) / len(grades) if grades else 0
    
    return gwa, execution_time, results


def run_comparison():
    """Run comprehensive comparison between multithreading and multiprocessing."""
    print("\n" + "="*70)
    print("GRADE COMPUTING SYSTEM - PERFORMANCE COMPARISON")
    print("="*70)
    
    # Get test data
    test_sizes = [10, 50, 100, 500]
    
    print("\nThis comparison will test both methods with different dataset sizes.")
    print("Test sizes:", test_sizes)
    
    results_table = []
    
    for size in test_sizes:
        print(f"\n{'='*70}")
        print(f"Testing with {size} subjects")
        print('='*70)
        
        # Generate sample data
        subjects_data = [(f"Subject_{i+1}", 75 + (i % 25)) for i in range(size)]
        
        # Test multithreading
        print(f"\n--- MULTITHREADING ({size} subjects) ---")
        mt_gwa, mt_time, mt_results = test_multithreading(subjects_data.copy())
        
        # Test multiprocessing
        print(f"\n--- MULTIPROCESSING ({size} subjects) ---")
        mp_gwa, mp_time, mp_results = test_multiprocessing(subjects_data.copy())
        
        # Store results
        results_table.append({
            'size': size,
            'mt_gwa': mt_gwa,
            'mt_time': mt_time,
            'mp_gwa': mp_gwa,
            'mp_time': mp_time,
            'speedup': mt_time / mp_time if mp_time > 0 else 0
        })
        
        print(f"\nResults for {size} subjects:")
        print(f"  Multithreading  - GWA: {mt_gwa:.2f}, Time: {mt_time:.6f}s")
        print(f"  Multiprocessing - GWA: {mp_gwa:.2f}, Time: {mp_time:.6f}s")
        print(f"  Speedup: {mt_time/mp_time:.2f}x {'(MT faster)' if mt_time < mp_time else '(MP faster)'}")
    
    # Display summary table
    print("\n" + "="*70)
    print("PERFORMANCE SUMMARY")
    print("="*70)
    print(f"{'Size':<8} {'MT Time (s)':<15} {'MP Time (s)':<15} {'Faster Method':<20}")
    print("-"*70)
    
    for result in results_table:
        faster = "Multithreading" if result['mt_time'] < result['mp_time'] else "Multiprocessing"
        print(f"{result['size']:<8} {result['mt_time']:<15.6f} {result['mp_time']:<15.6f} {faster:<20}")
    
    print("="*70)
    
    # Analysis
    mt_times = [r['mt_time'] for r in results_table]
    mp_times = [r['mp_time'] for r in results_table]
    
    print("\nKEY OBSERVATIONS:")
    print(f"1. Average MT Time: {statistics.mean(mt_times):.6f}s")
    print(f"2. Average MP Time: {statistics.mean(mp_times):.6f}s")
    print(f"3. MT wins in {sum(1 for r in results_table if r['mt_time'] < r['mp_time'])}/{len(results_table)} tests")
    print(f"4. MP wins in {sum(1 for r in results_table if r['mp_time'] < r['mt_time'])}/{len(results_table)} tests")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    run_comparison()
