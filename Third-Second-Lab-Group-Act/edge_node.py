import uuid
import random
import time
import requests

# Local Flask API URL
API_URL = "http://localhost:5000/vote"

# Unique ID for this edge node
NODE_ID = f"node-{random.randint(1, 100)}"

def generate_vote():
    return {
        "user_id": str(uuid.uuid4()),
        "poll_id": "poll_1",
        "choice": random.choice(["A", "B", "C"]),
        "timestamp": time.time(),
        "edge_id": NODE_ID,
        "time_created": time.time()
    }

def send_vote(vote, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, json=vote, timeout=5)
            if response.status_code == 200:
                print(f"[{NODE_ID}] Vote sent: {vote['user_id']} | Choice: {vote['choice']}")
                return
            else:
                print(f"[{NODE_ID}] Bad response: {response.status_code}, retrying...")
        except Exception as e:
            print(f"[{NODE_ID}] Failed (attempt {attempt+1}): {e}")
            time.sleep(2)
    print(f"[{NODE_ID}] All retries exhausted for: {vote['user_id']}")

def run_edge_node():
    print(f"Edge node {NODE_ID} starting...")
    while True:
        vote = generate_vote()
        send_vote(vote)
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    run_edge_node()