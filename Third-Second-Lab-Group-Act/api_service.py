import os
from pathlib import Path

from flask import Flask, request, jsonify
from supabase import create_client

app = Flask(__name__)


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

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env or the environment")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/vote", methods=["POST"])
def receive_vote():
    vote = request.get_json()

    # Validate
    if not vote:
        return jsonify({"error": "Invalid payload"}), 400
    for field in ["user_id", "poll_id", "choice"]:
        if field not in vote:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        # Insert into queue (simulates Pub/Sub publish)
        supabase.table("votes_queue").insert({
            "user_id": vote["user_id"],
            "poll_id": vote["poll_id"],
            "choice": vote["choice"],
            "edge_id": vote.get("edge_id"),
            "timestamp": vote.get("timestamp"),
            "time_created": vote.get("time_created"),
            "status": "pending"
        }).execute()
        return jsonify({"status": "accepted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "API is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)