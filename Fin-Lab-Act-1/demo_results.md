# Distributed Order Processing Demo

## Unsynchronized run 

```text
[WORKER 2] Assigned orders: [2, 5] [NO LOCK]
[WORKER 2] Processed order 2: Yellow Pad
[WORKER 2] Processed order 5: Correction Tape
[WORKER 3] Assigned orders: [3, 6] [NO LOCK]
[WORKER 3] Processed order 3: Pencil
[WORKER 3] Processed order 6: Eraser
[WORKER 1] Assigned orders: [1, 4] [NO LOCK]
[WORKER 1] Processed order 1: Ballpen
[WORKER 1] Processed order 4: Notebook
[MASTER] Generated orders:
	1: Ballpen
	2: Yellow Pad
	3: Pencil
	4: Notebook
	5: Correction Tape
	6: Eraser
[MASTER] Mode: UNSYNC

[MASTER] Completed orders (from shared list):
	Order 1 (Ballpen) handled by worker 1
	Order 2 (Yellow Pad) handled by worker 2
	Order 3 (Pencil) handled by worker 3
	Order 4 (Notebook) handled by worker 1
	Order 5 (Correction Tape) handled by worker 2
	Order 6 (Eraser) handled by worker 3
```

## Synchronized run 

```text
[WORKER 2] Assigned orders: [2, 5] [LOCKED]
[WORKER 2] Processed order 2: Yellow Pad
[WORKER 2] Processed order 5: Correction Tape
[WORKER 1] Assigned orders: [1, 4] [LOCKED]
[WORKER 1] Processed order 1: Ballpen
[WORKER 1] Processed order 4: Notebook
[WORKER 3] Assigned orders: [3, 6] [LOCKED]
[WORKER 3] Processed order 3: Pencil
[WORKER 3] Processed order 6: Eraser
[MASTER] Generated orders:
	1: Ballpen
	2: Yellow Pad
	3: Pencil
	4: Notebook
	5: Correction Tape
	6: Eraser
[MASTER] Mode: SYNC

[MASTER] Completed orders (from shared list):
	Order 1 (Ballpen) handled by worker 1
	Order 3 (Pencil) handled by worker 3
	Order 2 (Yellow Pad) handled by worker 2
	Order 4 (Notebook) handled by worker 1
	Order 6 (Eraser) handled by worker 3
	Order 5 (Correction Tape) handled by worker 2
```

## Explanation 

- Unsynchronized run:
	- Workers wrote to the shared list at the same time without asking permission.
	- Because writes can overlap, the final order of completed records is not predictable.

- Synchronized run:
	- Workers used a lock so only one could write at a time.
	- This made the final recorded order stable and repeatable across runs.

Why this matters
- When many processes share the same data, uncoordinated writes can give different results each run.
- A simple lock makes writes happen one-by-one, avoiding those unpredictable results.

