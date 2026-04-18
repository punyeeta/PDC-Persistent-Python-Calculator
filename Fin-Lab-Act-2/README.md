# Shonget PDC Answers

## Reflection and Analysis
1. Differences observed between sequential and parallel execution 
2. Performance behavior across dataset sizes 
3. Challenges encountered during implementation 
4. Insights about overhead, synchronization, or merging 
5. Situations where parallelism was beneficial or unnecessary

---

### Chiong, Heart
1. 
2. 
3. 
4. 
5. 

---

### Limpahan, Mark Vincent
1. Sequential execution consistently finished faster than parallel across both sorting and searching tasks, except for larger datasets where parallel sorting could be at advantage.
2. For sorting, the performance gap between sequential and parallel narrowed as dataset size grew. For searching, parallel never caught up regardless of dataset size, since linear search is too lightweight to justify the multiprocessing cost.
3. The main challenge was correctly computing the global index in parallel search, as each worker only knows its local position within its chunk, so the offset had to be added to return the correct position in the original dataset. For sorting, merging the sorted chunks back in the right order required careful handling.
4. Python's multiprocessing has significant startup overhead per process. For short tasks, this overhead dominates total runtime. The Queue in searching and the merge step in sorting both add synchronization cost that sequential execution simply doesn't have.
5. Parallelism showed its only clear benefit in sorting the large random dataset. It was unnecessary for searching entirely, and for small to medium datasets across both tasks, highlighting that parallelism is not always the right tool, problem size and task complexity also matter.

---

### Locsin, Roxanne
1. 
2. 
3. 
4. 
5. 

---

### Sajol, Rhenel Jhon
1. Sequential and parallel gave the same correct outputs, but their speed was different. In searching, sequential was always faster: for example, in large_random it was 0.012810s while parallel was 1.863798s. In sorting, sequential was faster in small_random (0.002174s vs 0.018173s) and medium_random (0.206448s vs 0.284572s), but parallel became faster in large_random (2.388788s vs 3.149599s).
2. As dataset size increased, runtime increased. For searching, sequential changed from 0.000021s (small_sorted) to 0.012810s (large_random), while parallel stayed much higher at about 0.539038s to 1.959237s because of process setup cost. For sorting, runtimes grew from around 0.001-0.018s at 1,000 elements to around 1.5-3.1s at 1,000,000 elements.
3. A challenge was setting up multiprocessing and dividing tasks correctly across processes. It was also difficult to ensure all workers finished correctly and produced the same final output. Another challenge was understanding why some runs were slower in parallel, especially on smaller datasets where overhead dominates.
4. The results show overhead is very important. In searching, parallel added about 0.5-1.9s extra cost even when sequential only needed 0.000021s to 0.012810s. In sorting, synchronization and merging of partitions added extra work, which is why parallel was slower for small/medium datasets and only improved when the workload was large enough.
5. Parallelism was beneficial in large random sorting (1,000,000 elements), where parallel quicksort took 2.388788s versus 3.149599s sequential. Parallelism was unnecessary for searching in this activity, since sequential was faster in all six datasets. It was also unnecessary for most small and medium sorting cases where overhead was bigger than the speed gain.

---

### Mag-isa, Jules
1. 
2. 
3. 
4. 
5. 

---
