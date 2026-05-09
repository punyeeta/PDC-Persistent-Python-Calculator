# PDF Requirements vs Our Supabase Implementation
 
---
 
## Phase 1: GCP Setup & System Configuration
 
| PDF (GCP) | Our Version (Supabase) | Status |
|---|---|---|
| Create GCP project | Create Supabase project |  Same idea |
| Enable Cloud Run, Pub/Sub, Firestore APIs | No API enabling needed — Supabase is ready out of the box |  Simpler |
| Create Firestore database (Native Mode, asia-southeast1) | Create `votes` table in Supabase (PostgreSQL) |  Same purpose |
| Create Pub/Sub topic: `vote-topic` | Create `votes_queue` table with status column |  Replaces Pub/Sub |
| Create subscription: `vote-sub` (Pull type) | Worker polls `votes_queue` for "pending" rows |  Replaces subscription |
 
> **Note:** GCP required billing even for free tier services. Supabase is completely free with no credit card required.
 
---
 
## Phase 2: Edge Computing (Client Nodes)
 
| PDF (GCP) | Our Version (Supabase) | Status |
|---|---|---|
| Each group member runs an independent edge node | Same — each member runs `edge_node.py` independently |  Identical |
| `generate_vote()` with user_id, poll_id, choice, timestamp | Same fields + added `edge_id` and `time_created` |  Enhanced |
| `send_vote()` with retry logic for network failures | Same retry logic with exponential backoff |  Identical |
| Random delays between votes (1–3 seconds) | Same random delays (1–3 seconds) |  Identical |
| Send via HTTP POST to Cloud Run API URL | Send via HTTP POST to local Flask API on `localhost:5000` |  Local instead of cloud |
 
> **Note:** This phase is almost identical. The only difference is the edge node sends to localhost instead of a deployed Cloud Run URL.
 
---
 
## Phase 3: Cloud Ingestion Layer (API)
 
| PDF (GCP) | Our Version (Supabase) | Status |
|---|---|---|
| Flask API deployed on Cloud Run | Flask API runs locally on `localhost:5000` |  Local, not deployed |
| Receive `POST /vote`, validate payload | Same — validate user_id, poll_id, choice |  Identical |
| Publish validated vote to Pub/Sub `vote-topic` | Insert vote into `votes_queue` with `status=pending` | Replaces Pub/Sub publish |
| Return 200 accepted immediately (non-blocking) | Same — return 200 immediately |  Identical |
| Publicly accessible via HTTPS URL | Only accessible within the same machine |  No public URL |
 
> **Note:** Biggest difference in this phase — the API runs locally instead of being deployed to the cloud. The logic is exactly the same, only the hosting is different.
 
---
 
## Phase 4: Distributed Processing Layer (Worker)
 
| PDF (GCP) | Our Version (Supabase) | Status |
|---|---|---|
| Worker deployed on Cloud Run | Worker runs locally as a Python script |  Local, not deployed |
| Subscribe to `vote-sub`, receive messages via Pub/Sub | Poll `votes_queue` every 2 seconds for pending rows |  Pull instead of push |
| Decode and parse each message | Same — parse each vote row |  Identical |
| Idempotency: `doc_id = user_id + poll_id` | Same idempotency key: `user_id + poll_id` |  Identical |
| Write to Firestore with `.set()` | Write to `votes` table using `.upsert()` |  Same concept |
| `message.ack()` on success, `nack()` on failure | Update status to "processed" (ack) or leave as pending (nack) |  Same concept |
 
> **Note:** The core logic is identical. The main difference is polling vs real push messaging — but the end result and behavior are the same.
 
---
 
## Phase 5: Fault Injection & System Behavior
 
| PDF (GCP) | Our Version (Supabase) | Status |
|---|---|---|
| Test 1: Send same vote twice (duplicate simulation) | Same — send same vote twice in `edge_node.py` |  Identical |
| Test 2: Set Cloud Run worker to 0 instances (worker failure) | Stop `worker_service.py` with Ctrl+C |  Manual stop instead of Cloud Run config |
| Test 3: Restore Cloud Run worker, observe recovery | Restart `worker_service.py`, observe it processes pending rows |  Same behavior |
| Observe Pub/Sub buffering votes during downtime | `votes_queue` rows stay as "pending" during downtime |  Same concept |
 
> **Note:** All 3 fault tests produce the same results. Instead of the Cloud Run console, you simply stop and start a Python script.
 
---
 
## Phase 6: System Evaluation & Performance Analysis
 
| PDF (GCP) | Our Version (Supabase) | Status |
|---|---|---|
| Measure end-to-end latency (edge to Firestore) | Same — worker prints latency in terminal automatically |  Identical |
| Evaluate throughput using Pub/Sub metrics dashboard | Count rows in `votes_queue` and `votes` tables |  Manual count instead of dashboard |
| Compare votes generated vs queued vs stored | Compare terminal logs vs Supabase table row counts |  Same concept |
| Analyze system trade-offs | Same trade-offs apply, just with Supabase instead of GCP |  Same analysis |
 
> **Note:** All evaluation steps work the same way. Instead of GCP dashboards, you use terminal logs and Supabase Table Editor to count and verify rows.

System Evaluation & Performance Analysis (step-by-step):

1. Prepare a clean workspace
	- In Supabase SQL Editor run `DELETE FROM votes;` and `DELETE FROM votes_queue;` to clear prior runs.

2. Start components
	- Terminal A: `python api_service.py 2>&1 | tee api_log.txt`
	- Terminal B: `python worker_service.py 2>&1 | tee worker_log.txt`
	- Terminal C: `python edge_node.py 2>&1 | tee edge_log.txt`

3. Run the workload for a fixed interval (e.g., 30–60s) and save logs from each terminal.

4. Record database counts
	- In Supabase run `SELECT COUNT(*) FROM votes_queue WHERE status='pending';` and `SELECT COUNT(*) FROM votes;`.

5. Compute metrics
	- Throughput: processed_count / run_duration (votes/sec).
	- Success rate: processed_count / generated_count.
	- Latency: extract `Latency: X.XXXs` lines from the worker log and compute min/median/mean/p90.

6. Fault-injection (optional)
	- Stop the worker while the edge node continues, then restart it and measure backlog recovery time and post-recovery latency.

Notes:
- Use `python worker_service.py --mock --once` for quick, offline verification.
- Keep run duration and generation rate consistent for fair comparisons.
 
---
 
## Phase 7: Reflection & Submission
 
| PDF (GCP) | Our Version (Supabase) | Status |
|---|---|---|
| Individual reflection paragraphs in README.md | Same — individual reflections in README.md |  Identical |
| Architecture diagram showing system flow | Same — architecture diagram showing new flow |  Same requirement |
| Demo GIF or video of system running | Same — screen record all 3 terminals running |  Identical |
| Cloud Run API endpoint URL | No deployed URL — noted in README that Supabase was used |  No public URL |
| GitHub repository with all components | Same — GitHub repository |  Identical |
 
> **Note:** The only missing piece is a public Cloud Run URL. This is noted in the README with an explanation that Supabase was used as an alternative approved by the professor.
 
---
 
## Overall Summary
 
| Category | Count |
|---|---|
|  Identical or same concept | 22 |
|  Different approach, same result | 10 |
|  Missing entirely | 0 |
 
### What stayed exactly the same
- Edge node behavior (independent, random delays, retry logic)
- Vote data structure and generation
- Payload validation in the API
- Idempotency key design (user_id + poll_id)
- All 3 fault injection tests
- Latency measurement
- README, diagram, and reflection requirements
### What changed (but achieves the same goal)
- Cloud Run → Local Flask (same API logic, different hosting)
- Pub/Sub → Supabase votes_queue table (same buffering behavior)
- Firestore → Supabase votes table (same persistent storage)
- Cloud Run scaling → Ctrl+C to simulate failure (same fault isolation effect)
- GCP metrics dashboard → Supabase Table Editor (same data visibility)
### Why we used Supabase
GCP requires billing account setup even for free tier services, which was not feasible for this lab. Supabase was suggested by the professor as a free alternative. All distributed system concepts from the lab — edge computing, message queuing, fault tolerance, idempotency, and eventual consistency — are fully demonstrated using this setup.
