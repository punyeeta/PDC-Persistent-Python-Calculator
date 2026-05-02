<img width="1152" height="648" alt="PDC_FinLab1" src="https://github.com/user-attachments/assets/b01ebe7a-d3ce-4ddf-99e4-12352b3bc784" />
# Shonget PDC Answers

## Reflection Questions

Provide written answers to the following questions: 
1. How did you distribute orders among worker processes? 
2. What happens if there are more orders than workers? 
3. How did processing delays affect the order completion? 
4. How did you implement shared memory, and where was it initialized? 
5. What issues occurred when multiple workers wrote to shared memory simultaneously? 
6. How did you ensure consistent results when using multiple processes? 

---

### Chiong, Heart
1. Round-robin method was the method we used to distribute the orders through the workers, where tasks are assigned one by one to each worker in order, then repeated.
2. If there are more orders than workers, some workers just handle multiple orders. All workers still run at the same time, so processing continues efficiently and balanced.
3. The delays made the finishing order random. Even if tasks were given in sequence, they didn’t finish in the same order because of different processing times.
4. We used a Manager to create a shared list that all processes can access. It was set up in the main process before the workers started.
5. When workers wrote at the same time, it caused conflicts in the shared data. Some outputs got messy or out of order.
6. To fix that, we added a lock so only one worker can write at a time, which kept the results correct and consistent.

---

### Limpahan, Mark Vincent
1. We distributed the orders using a round-robin method, where each order is assigned one by one to each worker in sequence. Once all workers have been assigned an order, the cycle repeats. This keeps the workload balanced across all workers.
2. If there are more orders than workers, some workers simply take on more than one order. All workers still run at the same time, so the extra load is handled efficiently without blocking other workers. The master process waits until all results are returned before finishing.
3. The processing delays caused the completion order to become unpredictable. Since each worker runs in parallel and has its own delay, tasks don't necessarily finish in the order they were assigned. The timing of each process determines which finishes first.
4. We used a Manager to set up a shared list that all worker processes can access. The shared memory was initialized by the main process before any workers were started, so all workers connect to the same centralized structure.
5. When multiple workers wrote to shared memory at the same time, race conditions occurred. Without any access control, the shared data could become inconsistent, with entries appearing out of order or getting overwritten.
6. We resolved this by using a lock that allows only one worker to write to the shared memory at a time. This prevents conflicts and ensures that the final output is complete, correct, and consistent across every run.

---

### Locsin, Roxanne
1. We used a round-robin approach to distribute the orders evenly across workers. Each order is assigned one by one, and once all workers receive an order, the assignment cycles back to the first worker. This ensures that the workload is balanced and no single worker is overloaded.
2. If there are more orders than workers, some workers simply receive more tasks, but the distribution remains balanced overall. Each worker processes its assigned orders sequentially, while all workers run concurrently. The system still works efficiently since no worker blocks others, and the master waits for all results before finishing.
3. Processing delays made the completion order non-deterministic. Since all workers run in parallel and each task includes a delay, the order in which tasks finish depends on timing rather than assignment. As a result, the output order can vary in each run even though the processing itself is correct.
4. We implemented shared memory using a Manager, which maintains a shared list accessible by all processes. This shared structure is initialized by the master process and managed in a separate process. Workers connect to it and update the shared list, allowing all results to be stored in a centralized location.
5. When multiple workers wrote to shared memory at the same time, race conditions occurred. This led to inconsistent outputs such as unordered or missing entries because there was no control over simultaneous access. As a result, the output became unpredictable across different runs.
6. We ensured consistency by using a lock to control access to the shared memory. Only one worker can write at a time, preventing conflicts and ensuring correct results. This made the final output stable, complete, and consistent in every execution.

---

### Sajol, Rhenel Jhon
1. We gave the orders to the workers one by one using round-robin, so the work was shared fairly and no worker got all the tasks at once. This is done in [main_activity.py](Fin-Lab-Act-1/main_activity.py) in the `assign_orders` function, where the orders are placed by index into each worker group.
2. If there were more orders than workers, some workers got more than one order, but all workers still kept working. The master still sends the jobs to each worker in [main_activity.py](Fin-Lab-Act-1/main_activity.py), so every order gets assigned even when the list is longer than the number of workers.
3. The delays changed the finish order, so some tasks finished faster than others even if they were assigned earlier. In [main_activity.py](Fin-Lab-Act-1/main_activity.py), each worker uses `time.sleep(1)` before writing the result, which makes the timing of each process matter.
4. We used shared memory with a Manager, and it was created in the main process before the workers started. You can see this in [main_activity.py](Fin-Lab-Act-1/main_activity.py) where `OrderManager` is started, `get_shared_orders` is registered, and the workers connect to the same manager address.
5. When many workers wrote at the same time, the data could mix up or become wrong. This problem is shown in [main_activity.py](Fin-Lab-Act-1/main_activity.py) when workers write with `shared_orders.append(rec)` without a lock, because the updates are not fully protected.
6. We used a lock so only one worker could write at a time, which kept the results correct and more stable. The safe write happens in [main_activity.py](Fin-Lab-Act-1/main_activity.py) through `append_record` and `use_lock`, so the shared list is updated in a controlled way.

---

### Mag-isa, Jules
1. Here, we used the round-robin approach, where each task for the workers happens one at a time, then repeated until all of them got their tasks completed.  
2. Though some orders are more than workers, there are some of those that run sequentially, and the rest are run concturrently. But good news is that the distribution still remains balanced. That's because no other blocks the others, and the master waits for them to finish.
3. The order completion (thanks to processing delays) will result in random orders for the workers. Which means that they did not get the desired order due to different processing times, even if they're given a sequence of orders.
4. We used Manager for implementing the shared memory for all processes to have the same list. This is initialized by the master process and it is managed by a seprate class. Thanks to a entralized location, workers can access connection and updates with the shared list, where all results can be stored there.
5. For the issues with simultaneous writing to shared memory from workers, we have race conditions; due to the fact that some of them have no orders, while others have missing ones, making the results inconsistent and messy to look at.
6. To make a remedy for inconsistent results in using multiple processes, we used a lock to control access to the shared memory. This allows a worker to access one at a time, making the results consistent, clean, and organized.

---
