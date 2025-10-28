import json
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = "logs/conversation_log.jsonl"

def _ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def log_event(event_type: str, data: dict):
    """
    event_type: "command", "llm", "error", etc
    data: dict with details

    writes one json line per event to logs/conversation_log.jsonl
    """
    _ensure_log_dir()

    entry = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "type": event_type,
        **data
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")