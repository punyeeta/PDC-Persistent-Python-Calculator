import os
import sys
import time
from pathlib import Path

# Determine mock mode before importing external dependencies
USE_MOCK = os.getenv("SUPABASE_MOCK", "0") == "1" or "--mock" in sys.argv
ONCE = "--once" in sys.argv

if not USE_MOCK:
    try:
        from supabase import create_client
    except Exception as e:
        print(f"Failed to import supabase client: {e}")
        sys.exit(1)

# Prefer environment variables for credentials. Set these before running:
# export SUPABASE_URL="https://<project>.supabase.co"
# export SUPABASE_KEY="<service_role_or_anon_key>"


def load_dotenv_file(dotenv_path: str = ".env") -> None:
    path = Path(dotenv_path)
    if not path.exists():
        return

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_dotenv_file()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not USE_MOCK:
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: SUPABASE_URL or SUPABASE_KEY not set.\n"
              "Set environment variables SUPABASE_URL and SUPABASE_KEY in .env or before running.\n"
              "Example .env entries:\n"
              "SUPABASE_URL=https://your-project.supabase.co\n"
              "SUPABASE_KEY=your-key")
        sys.exit(1)

    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Failed to create Supabase client: {e}")
        sys.exit(1)

if USE_MOCK:
    print("Starting in MOCK mode: simulating Supabase tables locally")

    class MockTable:
        def __init__(self, storage):
            self.storage = storage
            self._where = None
            self._limit = None

        def select(self, *_args, **_kwargs):
            return self

        def eq(self, key, value):
            self._where = (key, value)
            return self

        def limit(self, n):
            self._limit = n
            return self

        def execute(self):
            if self._where is None:
                data = list(self.storage)
            else:
                key, val = self._where
                data = [r for r in self.storage if r.get(key) == val]
            if self._limit:
                data = data[: self._limit]
            class R: pass
            r = R()
            r.data = data
            return r

        def upsert(self, obj):
            # Replace if id matches, else append
            for i, r in enumerate(self.storage):
                if r.get("id") == obj.get("id"):
                    self.storage[i] = obj
                    break
            else:
                self.storage.append(obj)
            class Exec:
                def __init__(self, data):
                    self.data = data

                def execute(self):
                    return self

            return Exec([obj])

        def update(self, patch):
            class Q:
                def __init__(self, storage, patch):
                    self.storage = storage
                    self.patch = patch
                    self._where = None

                def eq(self, key, value):
                    self._where = (key, value)
                    return self

                def execute(self):
                    if self._where:
                        k, v = self._where
                        for r in self.storage:
                            if r.get(k) == v:
                                r.update(self.patch)
                    class R: pass
                    rr = R()
                    rr.data = []
                    return rr

            return Q(self.storage, patch)

    class MockClient:
        def __init__(self):
            self._tables = {
                "votes_queue": [
                    {"id": "1", "user_id": "alice", "poll_id": "p1", "choice": "A", "status": "pending", "time_created": time.time() - 1},
                    {"id": "2", "user_id": "bob", "poll_id": "p1", "choice": "B", "status": "pending", "time_created": time.time() - 3},
                ],
                "votes": [],
            }

        def table(self, name):
            return MockTable(self._tables.setdefault(name, []))

    supabase = MockClient()


def process_votes():
    print("Worker started, listening for votes...")
    backoff = 1
    while True:
        try:
            # Fetch pending votes (simulates Pub/Sub pull)
            result = supabase.table("votes_queue") \
                .select("*") \
                .eq("status", "pending") \
                .limit(10) \
                .execute()

            # Reset backoff on success
            backoff = 1

            if not getattr(result, "data", None):
                # No pending items, sleep briefly
                time.sleep(2)
                if ONCE:
                    break
                continue

            for vote in result.data:
                try:
                    doc_id = f"{vote['user_id']}_{vote['poll_id']}"

                    if vote.get("time_created"):
                        latency = time.time() - vote["time_created"]
                        print(f"Latency: {latency:.3f}s | Vote: {vote['user_id']}")

                    supabase.table("votes").upsert({
                        "id": doc_id,
                        "user_id": vote["user_id"],
                        "poll_id": vote["poll_id"],
                        "choice": vote["choice"],
                        "edge_id": vote.get("edge_id"),
                        "timestamp": vote.get("timestamp"),
                        "time_created": vote.get("time_created")
                    }).execute()

                    supabase.table("votes_queue") \
                        .update({"status": "processed"}) \
                        .eq("id", vote["id"]) \
                        .execute()

                    print(f"Processed: {vote['user_id']} | Choice: {vote['choice']}")

                except Exception as e:
                    print(f"Error processing vote: {e}")

            if ONCE:
                break

        except Exception as e:
            print(f"Worker error: {e}")
            time.sleep(backoff)
            backoff = min(30, backoff * 2)
            continue


if __name__ == "__main__":
    process_votes()