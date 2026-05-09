import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    ("API", "api_service.py"),
    ("Worker", "worker_service.py"),
    ("Edge", "edge_node.py"),
]


def start_process(name: str, script: str) -> subprocess.Popen:
    print(f"Starting {name}: {script}")
    return subprocess.Popen(
        [sys.executable, str(ROOT / script)],
        cwd=ROOT,
    )


def main() -> int:
    processes = [start_process(name, script) for name, script in SCRIPTS]

    try:
        exit_codes = [process.wait() for process in processes]
    except KeyboardInterrupt:
        print("Stopping services...")
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            if process.poll() is None:
                process.wait()
        return 130

    return max(exit_codes) if exit_codes else 0


if __name__ == "__main__":
    raise SystemExit(main())