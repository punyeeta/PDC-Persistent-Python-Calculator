# Section: BSCS-3A
# Group Name: Shonget
# Group Members: Chiong, Limpahan, Locsin, Mag-Isa, Sajol

## Analysis Questions

1. Differentiate Task and Data Parallelism. Identify which part of the lab demonstrates each and justify the workload division. 
Task parallelism is when you run different tasks at the same time on the same data. In our lab, we did this when we calculated SSS, PhilHealth, Pag-IBIG, and Tax separately using ThreadPoolExecutor, the work is split by task type. While, data parallelism is when you run the same task on many pieces of data at the same time. In this activity, we applied one payroll function to all employees using ProcessPoolExecutor, hence the work is split by employee.

2. Explain how concurrent.futures managed execution, including submit(), map(), and Future objects. Discuss the purpose of with when creating an Executor. 
In Python, submit() is used to run a single task, and it returns a Future object, which stores the result until the task is finished. Meanwhile, map() is useful when you want to run the same function on multiple pieces of data at the same time, applying it concurrently to many inputs. Also, Future objects are helpful because they allow you to retrieve results later, after the task is done, without stopping the program. Finally, using with to create an executor makes managing tasks easier, since it automatically waits for all tasks to finish and frees resources when the work is complete.

3. Analyze ThreadPoolExecutor execution in relation to the GIL and CPU cores. Did true parallelism occur? 
ThreadPoolExecutor doesn’t run tasks truly in parallel for CPU-heavy work because of Python’s GIL, only one thread runs Python code at a time. Threads share CPU time, so multiple threads don’t fully use multiple cores for calculations like payroll.

4. Explain why ProcessPoolExecutor enables true parallelism, including memory space separation and GIL behavior. 
ProcessPoolExecutor uses separate processes, each process has its own memory and GIL, so they can really run at the same time on different CPU cores. That’s why it works well for CPU-heavy tasks.

5. Evaluate scalability if the system increases from 5 to 10,000 employees. Which approach scales better and why? 
Data parallelism is better for scaling. By using ProcessPoolExecutor, we can process many employees at once on multiple cores. Task parallelism doesn’t scale as well because it only splits small tasks for one employee and still runs into the GIL for CPU work.

6. Provide a real-world payroll system example. Indicate where Task Parallelism and Data Parallelism would be applied, and which executor you would use.
In a payroll system, data parallelism is used to calculate salaries for thousands of employees at the same time using ProcessPoolExecutor. While, task parallelism is used to calculate deductions, benefits, and generate reports for a single employee at the same time using ThreadPoolExecutor. With this, large payroll systems usually combine both approaches to make processing faster and more efficient.
