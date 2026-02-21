import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Simulated shared database lock
database_lock = threading.Lock()

# Simulated ID counter (shared resource)
id_counter = 0

# Function to simulate processing one applicant
def process_applicant(applicant_id):
    global id_counter
    
    # Step 1: Verify documents
    time.sleep(0.1)
    
    # Step 2: Encode data
    time.sleep(0.1)
    
    # Step 3: Capture photo
    time.sleep(0.1)
    
    # Step 4: Print ID
    time.sleep(0.1)
    
    # Critical Section: Assign unique ID and update database
    with database_lock:
        id_counter += 1
        assigned_id = id_counter
        time.sleep(0.05)  # simulate database writing delay
    
    return assigned_id

# Sequential Processing
def sequential_processing(applicants):
    global id_counter
    id_counter = 0

    start_time = time.time()

    for applicant in applicants:
        process_applicant(applicant)

    end_time = time.time()

    return end_time - start_time

# Parallel Version
def parallel_processing(applicants, workers=4):
    global id_counter
    id_counter = 0
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(process_applicant, applicants)
    
    end_time = time.time()
    
    return end_time - start_time

# -------------------------------
# Main Execution
# -------------------------------
if __name__ == "__main__":
    
    number_of_applicants = 20
    applicants = list(range(1, number_of_applicants + 1))
    
    print("Simulating Government ID Processing System")
    print("Number of Applicants:", number_of_applicants)
    print("-----------------------------------------")
    
    # Run Sequential
    seq_time = sequential_processing(applicants)
    print("Sequential Execution Time:", round(seq_time, 4), "seconds")
    
    # Run Parallel
    par_time = parallel_processing(applicants, workers=4)
    print("Parallel Execution Time:", round(par_time, 4), "seconds")
    
    # Calculate Speedup
    speedup = seq_time / par_time
    print("Speedup:", round(speedup, 2))
    
    print("-----------------------------------------")
    
    # Check scaling
    ideal_speedup = 4
    print("Ideal Speedup (4 threads):", ideal_speedup)
    
    if speedup < ideal_speedup:
        print("Result: Not ideal scaling due to synchronization and shared resources.")
    else:
        print("Result: Near ideal scaling.")



