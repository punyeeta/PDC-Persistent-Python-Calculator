# CS323 Distributed Voting System
### Laboratory Activity 2 | CS323 - Distributed Systems
**Group:** Shonget
**Members:**
- Chiong, Heart
- Limpahan, Mark Vincent
- Locsin, Roxanne
- Mag-isa, Jules
- Sajol, Rhenel Jhon

---

## System Overview

This project implements a Distributed Voting System that simulates an edge-to-cloud architecture. Multiple independent edge nodes generate votes and transmit them to a central API, which queues them for asynchronous processing by a worker service. All data is stored persistently in a Supabase database.

Since GCP required billing, the system was adapted to use Supabase as a free alternative, maintaining the same distributed system principles and architecture defined in the laboratory activity.

The system was designed and tested under both normal and failure conditions to evaluate its reliability, fault tolerance, and consistency as a distributed system.

---

## Architecture

```
Edge Nodes → Flask API → Supabase votes_queue → Worker Service → Supabase votes
```

| Component | Original (GCP) | Our Implementation |
|---|---|---|
| Edge Nodes | Python edge scripts | Python edge scripts |
| Ingestion Layer | Cloud Run API | Local Flask API |
| Message Queue | Google Pub/Sub | Supabase votes_queue table |
| Processing Layer | Cloud Run Worker | Local Python Worker |
| Storage Layer | Firestore | Supabase votes table |

### Component Descriptions

- **Edge Nodes** — Simulate distributed clients that independently generate and transmit votes. Each node has a unique ID, introduces random delays, and includes retry logic for failed transmissions.

- **Flask API** — A lightweight stateless REST API that receives vote data via HTTP POST, validates the payload, and inserts it into the Supabase queue table. This simulates the Cloud Run ingestion layer and Pub/Sub publish step.

- **Supabase votes_queue** — Acts as the message buffer between the API and worker. Votes are inserted with a `pending` status and updated to `processed` after the worker handles them. This simulates Google Pub/Sub behavior.

- **Worker Service** — Continuously polls the queue for pending votes, processes them, and writes the final result to the votes table using an idempotent upsert. This simulates the Cloud Run worker and Firestore write step.

- **Supabase votes** — The final persistent storage layer. Each document is uniquely identified by `user_id_poll_id` to prevent duplicate entries, simulating Firestore's document model.

---

## Architecture Diagram

![Architecture Diagram](diagram.png)

> *See diagram.png in the repository for the full system flow illustration.*

---

## Setup Instructions

### Requirements
- Python 3.8 or higher
- pip
- Supabase account (free at [supabase.com](https://supabase.com))
- Internet connection

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/[your-group]/cs323-voting-system
cd cs323-voting-system
```

---

### Step 2: Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line.

---

### Step 3: Install Dependencies

```bash
pip install supabase flask requests
```

---

### Step 4: Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project named `cs323-voting-system`
3. Go to **SQL Editor** and run the following:

```sql
-- Queue table (simulates Pub/Sub)
CREATE TABLE votes_queue (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  poll_id TEXT NOT NULL,
  choice TEXT NOT NULL,
  edge_id TEXT,
  timestamp FLOAT,
  time_created FLOAT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Final votes table (simulates Firestore)
CREATE TABLE votes (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  poll_id TEXT NOT NULL,
  choice TEXT NOT NULL,
  edge_id TEXT,
  timestamp FLOAT,
  time_created FLOAT,
  processed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Disable RLS for both tables
ALTER TABLE votes_queue DISABLE ROW LEVEL SECURITY;
ALTER TABLE votes DISABLE ROW LEVEL SECURITY;

-- Optional cleanup before running the demo again
-- Use this if you want a fresh start and no old rows left in the tables
DELETE FROM votes;
DELETE FROM votes_queue;
```

4. Go to **Project Settings → API** and copy:
   - **Project URL**
   - **Publishable (anon) Key**

---

### Step 5: Add Supabase Credentials

Create a `.env` file in this folder and add your Supabase values:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-publishable-key
SUPABASE_MOCK=0
```

Both `api_service.py` and `worker_service.py` read these values automatically when they start.

---

### Step 6: Run the System

Open **3 separate terminals**, activate venv in each, then run in this order:

```bash
# Terminal 1 — Start API first
python api_service.py
# Terminal 1 — With Time (60 secs sample)
timeout 60 python api_service.py 2>&1 | tee api_log.txt

# Terminal 2 — Start Worker
python worker_service.py
# Terminal 2 — With Time (60 secs sample)
timeout 60 python worker_service.py 2>&1 | tee worker_log.txt

# Terminal 3 — Start Edge Node
python edge_node.py
# Terminal 3 — With Time (60 secs sample)
timeout 60 python edge_node.py 2>&1 | tee edge_log.txt

```

If you want a single command instead, run:

```bash
python main.py
```

That starts the API, worker, and edge node together as separate processes.

If you want to test the worker without real Supabase data, run:

```bash
python worker_service.py --mock --once
```

---

### Step 7: Verify the System

1. Go to **Supabase → Table Editor**
2. Open `votes_queue` — you should see votes arriving with status `pending` first, then `processed` after the worker handles them
3. Open `votes` — you should see the final processed vote records being written by the worker service
4. Use the terminal logs from the API, worker, and edge node to confirm the end-to-end flow

---

## Fault Tolerance Tests

### Test 1: Message Duplication
Modified `edge_node.py` to send the same vote twice:
```python
vote = generate_vote()
send_vote(vote)
send_vote(vote)  # intentional duplicate
```
**Result:** The `votes` table still shows only one record per user because of the idempotency key `user_id_poll_id`. Duplicate messages are safely ignored.

---

### Test 2: Worker Failure
Stopped the worker service while edge nodes continued running.

**Observed:**
- Flask API continued accepting votes normally
- `votes_queue` accumulated votes with status `pending`
- `votes` table stopped receiving updates
- No system-wide crash occurred

This demonstrates how the queue isolates failure to a single component.

---

### Test 3: Recovery
Restarted the worker service after the failure period.

**Observed:**
- Worker automatically reconnected and began processing queued messages
- All pending votes were processed in batches
- `votes` table resumed updating without any manual intervention
- No votes were lost during the downtime period

---

## Performance Observations

This is the analysis phase. Use the live terminals and Supabase Table Editor to compare the flow from edge node to API to worker to database.

### Where to do the analysis

- **Terminal 1**: Check the API output to see each vote being accepted and inserted into `votes_queue`
- **Terminal 2**: Check the worker output to see each pending vote being processed and written into `votes`
- **Terminal 3**: Check the edge node output to see how many votes were generated and sent
- **Supabase Table Editor**: Open `votes_queue` and `votes` to count rows and confirm the status changes

### How to do the analysis

1. Run `api_service.py`, `worker_service.py`, and `edge_node.py` in separate terminals.
2. Let the edge node send votes for a short period.
3. Open Supabase Table Editor and compare the row counts in `votes_queue` and `votes`.
4. Compare the terminal logs with the table contents to confirm:
  - how many votes were generated
  - how many were queued
  - how many were processed successfully
5. Record the latency values printed by the worker and use them in your final report.

### What to measure

- Votes generated by the edge node
- Votes accepted by the API
- Votes still pending in `votes_queue`
- Votes processed into `votes`
- Latency printed by the worker

### End-to-End Latency
Latency was measured from `time_created` in the edge node to processing time in the worker.

| Condition | Avg Latency |
|---|---|
| Normal operation | ~0.3 - 0.6 seconds |
| After worker recovery | ~0.1 - 0.2 seconds (batch processing) |

### Throughput
| Layer | Count |
|---|---|
| Votes generated (edge) | [fill in after running] |
| Votes queued (votes_queue) | [fill in after running] |
| Votes processed (votes) | [fill in after running] |

---

## Demo

![System Demo](demo.gif)

> *See demo.gif in the repository for a live demonstration of the system.*

---

## Individual Reflections

### Chiong, Heart

[Write 2-3 paragraphs based on your actual experience. Discuss what you observed during normal operation, what happened during fault injection, and what you learned about distributed systems. Do not write theoretical explanations — focus on what you actually saw happen in the terminals and Supabase tables.]

---

### Limpahan, Mark Vincent

Running these terminals made distributed systems feel real for me in a way that you can only see when you're actually hands-on doing the lectures discussed. Watching the edge node send votes, the API accept them, and the worker drain the queue  made loose coupling click. I kept refreshing the Supabase Table Editor and seeing rows flip from `pending` to `processed`, and it was a simple thing that actually said a lot about how the system was designed.

The fault tolerance tests were where I learned the most. Seeing the API keep accepting votes without any issue while the worker was down showed me that the queue is not just a convenience. The duplication test was equally surprising because the `votes` table count never changed no matter how many duplicate votes were sent, and the idempotency key handled it completely silently. When the worker came back online and processed everything on its own, it confirmed that recovery does not have to be complicated if the architecture is set up right. The biggest shift in how I think about systems after this activity is that reliability is not about preventing failure, butabout making sure failure stays contained and recoverable. That idea became very concrete here, and I do not think I would have understood it the same way without actually watching it happen in the terminals.

---

### Locsin, Roxanne
[Write 2-3 paragraphs based on your actual experience. Discuss what you observed during normal operation, what happened during fault injection, and what you learned about distributed systems. Do not write theoretical explanations — focus on what you actually saw happen in the terminals and Supabase tables.]

---

### Mag-isa, Jules

[Write 2-3 paragraphs based on your actual experience. Discuss what you observed during normal operation, what happened during fault injection, and what you learned about distributed systems. Do not write theoretical explanations — focus on what you actually saw happen in the terminals and Supabase tables.]

---

### Sajol, Rhenel Jhon

When I started `api_service.py`, `worker_service.py`, and `edge_node.py` in three separate terminals, I watched how they worked together without needing to know about each other. The `edge_node.py` sent votes every few seconds, and the API accepted them with "POST /vote HTTP/1.1 200" responses. The worker just kept checking the queue by printing messages. When I opened `votes_queue` in Supabase, I saw something interesting happening in real time - new rows appeared with `status='pending'`, and then a few seconds later the status changed to 'processed' as the worker picked them up. The most important observation was after running for 60 seconds, I checked the database and found 22 votes in the `votes` table with 0 rows still pending. Every vote had traveled through the entire system smoothly from `edge_node.py` to `api_service.py` to `votes_queue` to `worker_service.py` and finally to the `votes` table.

The real lesson came when I stopped `worker_service.py` using Ctrl+C while letting `edge_node.py` continue sending votes. For about 15 seconds, the API kept accepting votes normally and they piled up in `votes_queue` with `status='pending'`. What surprised me was that nothing broke - the API did not crash, `edge_node.py` did not give up, and votes did not disappear. Then I restarted the worker by running `worker_service.py` again, and it immediately started processing all those waiting votes without any help from me. Looking at the code in `api_service.py` and `worker_service.py`, I realized they do completely different jobs but they communicate through the same `votes_queue` table using the status column. The API only cares about inserting data, and the worker only cares about reading and updating. Neither one needs to check if the other is working at that exact moment. This separation is what makes the system strong and able to handle problems. If one part breaks, the other keeps working and the queue holds everything safe until the broken part comes back online.



---


## Repository Structure

```
cs323-voting-system/
├── edge_node.py          # Edge node simulation
├── api_service.py        # Flask API (simulates Cloud Run ingestion)
├── worker_service.py     # Worker service (simulates Cloud Run worker)
├── diagram.png           # System architecture diagram
├── demo.gif              # System demo recording
└── README.md             # This file
```

---

## Trade-off Analysis

| Design Decision | Benefit | Trade-off |
|---|---|---|
| Supabase queue as Pub/Sub | Free, no billing needed | Polling adds slight delay vs real Pub/Sub push |
| Idempotent upsert | Prevents duplicate votes | Slight processing overhead per vote |
| Random edge delays | Simulates real distributed behavior | Makes throughput unpredictable |
| Retry logic in edge node | Handles network failures | May cause intentional duplicates during testing |
| Stateless Flask API | Fast, lightweight ingestion | No local processing, fully dependent on Supabase |
