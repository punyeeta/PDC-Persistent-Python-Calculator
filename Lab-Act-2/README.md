# Grade Computing System - Lab Report

## Group Members
[Chiong, Heart]
[Limpahan, Mark]
[Locsin, Roxanne]
[Sajol, Rhenel]

## Overview
This project implements a Grade Computing System using both **multithreading** and **multiprocessing** in Python. The system calculates the General Weighted Average (GWA) for multiple subjects, demonstrating concurrent execution patterns and performance differences.

## Project Structure
```
.
├── multithreading_gwa.py    # Multithreading implementation
├── multiprocessing_gwa.py   # Multiprocessing implementation
├── comparison.py            # Performance comparison script
└── README.md                # This file
```

## How to Run

### Run Multithreading Version
```bash
python multithreading_gwa.py
```

### Run Multiprocessing Version
```bash
python multiprocessing_gwa.py
```

### Run Performance Comparison
```bash
python comparison.py
```

## Performance Results

### Sample Execution Table

| Method            | Execution Order | GWA Output | Execution Time |
|-------------------|----------------|------------|----------------|
| Multithreading    | Non-deterministic (varies each run) | 86.25 | 0.012345s |
| Multiprocessing   | Non-deterministic (varies each run) | 86.25 | 0.045678s |

**Note:** Execution times will vary based on system specifications and number of subjects.

## Answers to Lab Questions

### 1. Which approach demonstrates true parallelism in Python? Explain.

**Multiprocessing** demonstrates true parallelism in Python.

**Explanation:**
**Multiprocessing** runs tasks in separate processes, each with its own Python interpreter and memory space. Because these processes are independent, they can execute on multiple CPU cores at the same time, allowing true parallel execution. In contrast, **multithreading** in Python is restricted by the Global Interpreter Lock (GIL) which allows only one thread to execute Python bytecode at a time. As a result, multithreading provides concurrency but not true parallelism for CPU-bound tasks, whereas multiprocessing enables tasks to run simultaneously across different CPU cores.

### 2. Compare execution times between multithreading and multiprocessing.

Based on our testing:
Our performance tests show that multithreading is dramatically faster than multiprocessing across all dataset sizes. With 10 subjects, multithreading completed in 0.007 seconds versus 0.362 seconds for multiprocessing (50x faster). At 50 subjects, the times were 0.008 seconds versus 1.370 seconds (171x faster). For 100 subjects, multithreading took 0.022 seconds compared to 2.862 seconds for multiprocessing (130x faster), and with 200 subjects, the gap widened to 0.041 seconds versus 5.766 seconds (140x faster).

Overall, multithreading averaged 0.020 seconds while multiprocessing averaged 2.590 seconds, with multithreading winning all 4 out of 4 tests. The massive time difference is due to multiprocessing's high overhead—creating separate processes, allocating individual memory spaces, and managing inter-process communication are all time-consuming operations. Since our GWA calculation involves minimal computation and is primarily I/O-bound (printing output), the overhead of multiprocessing far outweighs any benefits, making multithreading the superior choice for this task.

### 3. Can Python handle true parallelism using threads? Why or why not?

**No, Python cannot handle true parallelism using threads for CPU-bound tasks.**

**Explanation**
This is mainly because of the **Global Interpreter Lock (GIL)**. The GIL is a mechanism that allows only one thread to execute Python bytecode at a time, even on systems with multiple CPU cores. It exists to simplify memory management, since Python uses reference counting, which is not thread-safe, and to ensure compatibility with many C extensions that were not designed for multi-threaded execution.

However, Python threads can still be useful in certain cases. For **I/O-bound tasks** such as file reading, database access, or network requests, the GIL is released while waiting for I/O, allowing other threads to run. This means threads provide **concurrency**, but not true **parallelism**, for CPU-intensive programs. Some libraries like NumPy can achieve parallelism because they release the GIL during heavy computations.

In summary, Python threads run one at a time for CPU-bound code, switching quickly between tasks, rather than running simultaneously in parallel.

### 4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why?
**Explanation**
When testing with large numbers of grades, multithreading is significantly faster than multiprocessing. In our experiments with up to 200 subjects, multithreading consistently outperformed multiprocessing. For example, processing 200 grades took 0.041 seconds with multithreading versus 5.766 seconds with multiprocessing, making multithreading over 140 times faster. When we attempted to test with datasets approaching 1000 grades, the terminal would freeze and become unresponsive, particularly with multiprocessing, preventing us from completing those tests.

Multithreading is faster because it has minimal overhead—all threads share the same memory space and Python interpreter, making creation and communication nearly instantaneous. In contrast, multiprocessing requires creating separate processes, each with its own memory space and interpreter, which consumes significant system resources. On Windows, creating 200+ processes means allocating substantial memory and managing complex inter-process communication through Queues, resulting in major slowdowns. Additionally, our GWA calculation is an I/O-bound task (mostly printing output) with trivial computation, so we don't benefit from multiprocessing's true parallelism but still suffer from its overhead. The freezing at 1000+ grades occurs because spawning that many processes overwhelms system resources—each process consumes 10-50 MB of memory, and managing thousands of processes exhausts RAM and strains the operating system's scheduler.

### 5. Which method is better for CPU-bound tasks and which for I/O-bound tasks?

**CPU-bound tasks** are better handled using multiprocessing because they spend most of their time performing computations such as mathematical operations, data processing, or model training. Multiprocessing allows the program to fully use multiple CPU cores and avoids the limitations of the GIL, resulting in faster execution for computation-heavy workloads.

On the other hand, **I/O-bound tasks** are more suitable for multithreading since they mostly involve waiting for operations like file access, network requests, or user input. Multithreading works efficiently in these cases because threads can run while others are waiting, and the GIL is released during I/O operations, improving overall responsiveness.

In the case of our GWA Calculator, the task is primarily I/O-bound due to input and output operations, making multithreading the more appropriate and efficient choice.

### 6. How did your group apply creative coding or algorithmic solutions in this lab?

**Creative Implementations:**

1. **Thread-Safe Result Collection**
   - Used `threading.Lock` for thread-safe list operations
   - Used `multiprocessing.Queue` for process-safe communication
   - Ensures no data loss or race conditions

2. **Enhanced User Experience**
   - Input validation (grade range 0-100, positive numbers)
   - Formatted output with visual separators
   - Clear progress indicators
   - Subject name tracking (not just grades)

3. **Type Hints and Documentation**
   - Added type annotations for better code clarity
   - Comprehensive docstrings for all functions
   - Improved code readability and maintainability

4. **Performance Comparison Tool**
   - Created automated comparison script
   - Tests multiple dataset sizes (10, 50, 100, 500)
   - Calculates speedup ratios
   - Generates statistical summaries

5. **Modular Design**
   - Separated concerns (input, processing, output)
   - Reusable functions for GWA calculation
   - Easy to extend for weighted averages or different grading systems

6. **Error Handling**
   - Graceful handling of invalid inputs
   - Try-except blocks for user input
   - Edge case handling (empty grades list)

7. **Algorithmic Efficiency**
   - Minimal computation in worker threads/processes
   - Batch result collection
   - Efficient data structures (lists, queues)

## Key Learnings / Takeaway

Through this activity, we gained a clearer understanding of how concurrency works in practice and how it differs from parallelism. We observed that although both multithreading and multiprocessing allow tasks to run concurrently, their behavior and performance vary depending on the nature of the task. In particular, Python’s Global Interpreter Lock (GIL) limits true parallel execution in multithreading for CPU-bound tasks, while multiprocessing allows processes to run simultaneously across multiple cores. We also learned that execution order is not guaranteed in concurrent programs, as task completion depends on system scheduling and timing rather than input sequence. Overall, this exercise emphasized the importance of identifying whether a task is CPU-bound or I/O-bound before choosing an appropriate concurrency approach. Based on our observations, multithreading was more suitable for the GWA calculator since the task involved minimal computation and was primarily I/O-bound, making it simpler and more efficient for this use case.
