---
title: Graceful, Specific Error Handling
description: When handling failures, prefer predictable, safe behavior over broad
  or crash-prone exception handling—especially around filesystem, JSON parsing, network
  calls, and user/CLI boundaries.
repository: TauricResearch/TradingAgents
label: Error Handling
language: Python
comments_count: 7
repository_stars: 71953
---

When handling failures, prefer predictable, safe behavior over broad or crash-prone exception handling—especially around filesystem, JSON parsing, network calls, and user/CLI boundaries.

Practical rules:
1) Handle “expected missing” safely (filesystem)
- Don’t assume optional companion files exist (e.g., DB + -wal/-shm). Check existence before unlinking (or use missing_ok where available).

2) Degrade gracefully on corrupted/unreadable data (JSON/parse)
- Wrap JSON reads/parses in narrow try/except (JSONDecodeError, OSError). On failure, start fresh instead of crashing.
- When writing persistence, avoid partial/corrupt files by writing to a temp path and replacing.

3) Narrow exception types for network/API
- Catch only request/network exceptions (e.g., requests.exceptions.RequestException) when calling external services; avoid catch-all Exception unless the code truly treats every error as equivalent.

4) Use consistent, cross-platform encodings for text I/O
- When writing logs/output files, open with encoding="utf-8" to avoid Windows codec failures.

Example pattern:
```python
from pathlib import Path
import json
import requests

def clear_checkpoint_files(data_dir: Path) -> int:
    cp_dir = data_dir / "checkpoints"
    for db in cp_dir.glob("*.db"):
        for p in (db, db.with_name(f"{db.name}-wal"), db.with_name(f"{db.name}-shm")):
            if p.exists():
                p.unlink()
    return 0

def load_persisted(path: Path) -> dict:
    try:
        if not path.exists():
            return {"situations": [], "recommendations": []}
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # Corrupt/unreadable → safe default
        return {"situations": [], "recommendations": []}

def save_persisted(path: Path, payload: dict) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)

def fetch_with_best_effort(url: str) -> dict | None:
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return None

# Cross-platform log write
# with open(log_file, "a", encoding="utf-8") as f:
#     f.write(...)
```

Result: the app won’t crash on common real-world failure scenarios, errors are easier to reason about (because exceptions are specific), and behavior remains consistent across platforms and environments.