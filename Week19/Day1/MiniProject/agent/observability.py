"""Structured, secret-free logging of every tool call (JSONL file + in-memory events for the UI)."""
import json
import re
import time
from pathlib import Path

SECRET_PATTERNS = [r"gsk_[A-Za-z0-9]{10,}", r"sk-[A-Za-z0-9]{10,}", r"ghp_[A-Za-z0-9]{10,}",
                   r"(?i)(api[_-]?key|token|password|secret)[\"']?\s*[:=]\s*[\"']?[^\s\"',}]+"]


def redact(text: str) -> str:
    for p in SECRET_PATTERNS:
        text = re.sub(p, "[REDACTED]", text)
    return text


def summarize(value, limit=300) -> str:
    s = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
    s = redact(re.sub(r"\s+", " ", s))
    return s if len(s) <= limit else s[:limit] + f"… (+{len(s) - limit} chars)"


class RunLogger:
    def __init__(self, log_dir: Path):
        log_dir.mkdir(parents=True, exist_ok=True)
        self.path = log_dir / f"run_{time.strftime('%Y%m%d_%H%M%S')}.jsonl"
        self.events = []

    def log(self, kind: str, **data):
        event = {"ts": time.strftime("%H:%M:%S"), "kind": kind, **{k: summarize(v) if k in ("args", "result", "error", "text") else v for k, v in data.items()}}
        self.events.append(event)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        return event
