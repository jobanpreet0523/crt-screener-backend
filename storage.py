# storage.py
import json
from datetime import datetime

RESULT_FILE = "scan_results.json"


def save_results(results):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "results": results
    }

    with open(RESULT_FILE, "w") as f:
        json.dump(payload, f)


def load_results():
    try:
        with open(RESULT_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"results": []}
