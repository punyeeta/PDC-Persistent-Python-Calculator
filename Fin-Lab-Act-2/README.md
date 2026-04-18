# Execution Demo
<img width="1152" height="648" alt="PDC GIF" src="https://github.com/user-attachments/assets/8c44ec7e-0f62-46b2-985d-e844d415bff3" />


# Shonget PDC Answers

## Reflection and Analysis
1. Differences observed between sequential and parallel execution 
2. Performance behavior across dataset sizes 
3. Challenges encountered during implementation 
4. Insights about overhead, synchronization, or merging 
5. Situations where parallelism was beneficial or unnecessary

---

### Chiong, Heart
1. Sequential execution is simple and processes data one step at a time with no setup needed. Parallel splits the data across multiple processes running simultaneously, which adds complexity through coordination and synchronization. The biggest takeaway is that parallel does not automatically mean faster, it just means more moving parts.
2. Sequential won every search test by a huge margin, finishing in under 0.013s even on the largest dataset while parallel never went below 0.5s due to process startup costs. For sorting, parallel only started catching up on the large random dataset (2.39s vs 3.15s), showing that parallelism only helps when the workload is actually heavy. Python's built-in sorted() beat both in almost every case.
3. The trickiest part was returning the correct global index in parallel search. Since each worker only sees its own chunk, we had to pass an offset and return offset + i instead of just i. We also had to make sure every process puts something in the Queue even if the result is 1, otherwise the main process would hang waiting forever.
4. Parallel overhead is real and significant. Spawning processes alone cost nearly 2 seconds in some tests, completely burying the actual search time. Merging sorted chunks back together also adds extra work that sequential never deals with. Synchronization using join() and Queue worked correctly but still contributed to the slower runtime overall.
5. For searching, parallelism was unnecessary across all tests since overhead always dominated. For sorting, it only showed a slight benefit on the large random dataset. Parallelism would be worth it for much larger datasets or heavier computations, but for the sizes we tested, sequential was the smarter and faster choice almost every time.

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
1. Sequential and parallel gave the same correct outputs for sorting, but their speed was different. Sequential was faster for small random (0.002174s vs 0.018173s), medium random (0.206448s vs 0.284572s), small sorted (0.001137s vs 0.068730s), medium sorted (0.123600s vs 0.147476s), and large sorted (1.565447s vs 1.621215s). Parallel only became faster in large random, where it took 2.388788s compared to 3.149599s for sequential.
2. As dataset size increased, sorting runtime also increased. For random data, sequential grew from 0.002174s at 1,000 elements to 3.149599s at 1,000,000 elements, while parallel grew from 0.018173s to 2.388788s. For sorted data, both versions were still affected by size, but sequential remained faster in all three cases.
3. A challenge for me was during my parallel sorting implementation was dividing the dataset correctly across processes and then combining the sorted parts back into one final sorted output. It was also difficult to make sure every worker finished properly and that the parallel version still produced the same correct result as the sequential version. Another challenge was understanding why the parallel version was slower on smaller datasets, since process overhead can outweigh the benefit of splitting the work.
4. The results show overhead is very important in sorting. Synchronization and merging of partitions added extra work, which is why parallel was slower for small and medium datasets like small random, medium random, small sorted, medium sorted, and large sorted. Parallel only improved when the workload was large enough, as shown by large random.
5. Parallelism was beneficial only in large random sorting, where parallel quicksort took 2.388788s versus 3.149599s sequential. It was unnecessary for small random, medium random, small sorted, medium sorted, and large sorted because sequential sorting was still faster in those cases.

---

### Mag-isa, Jules
1. Sequential algorithm gave me about 0-1 second in performance while parallel lowered from 5-4 for 10,000. As for 1,000,000, sequential increased from 0 to 30 seconds while parallel is about 31 to 47 seconds, and for 1,000, sequential and parallel are about 0.000106 to 0.009940 and 2.431 to 2.043, respectively.  
2. The performance between them was uniquely different. Sequential algorithms increase in time to perform as datasizes increase while parallel algorithms decrease at the same increasing datasize. 
3. Challenges in implementing the algorithms was more about debugging. Honestly, troubleshooting errors by debugging took us some valueable time, especially for lab activities like this when time and performance counts.
4. On overhead, sequemtial algorithm is worse when the datasize increases, thus consuming time to sort the values in ascending order, while parallelism is best to save time. Merging is almost the same as you have to put them in closer values before arranging them chronologically. Synchronization? Well, that's already when two different groups of algorithms are in one file together, nothing much other than that.
5.P Paralelism is best when data sizes are large and you want to complete the algorithm in a short time span as possible, and not necessary when your datasize is small in value (less than a million or so).

---
