---
title: Idempotent, Safe Errors
description: Handle errors in a way that (a) doesn’t hide real bugs, (b) supports
  reruns after interruptions, and (c) degrades gracefully when data/operations are
  incomplete.
repository: awslabs/agentcore-samples
label: Error Handling
language: Python
comments_count: 3
repository_stars: 3244
---

Handle errors in a way that (a) doesn’t hide real bugs, (b) supports reruns after interruptions, and (c) degrades gracefully when data/operations are incomplete.

**1) Narrow exception handling**
- Avoid `except Exception` for operational logic; catch the specific exceptions you expect (e.g., `botocore.exceptions.ClientError`, `json.JSONDecodeError`, timeouts).
- If you must catch broadly, re-raise for unexpected/likely-programming errors.

**2) Make async create+poll flows idempotent**
- Persist newly created identifiers immediately after `create_*` succeeds (write env updates / state) *before* starting any `wait_for_status`/polling that could be interrupted.
- This prevents reruns from not knowing the resource already exists and trying to recreate it.

**3) Gracefully degrade on expected data failures**
- When optional/incomplete data is common (e.g., S3 recordings missing/corrupted), return a minimal fallback structure so the UI/service keeps running rather than crashing.
- Log/print a clear reason and keep the fallback shape stable.

**Example pattern (combined)**
```python
import time
import json
import boto3
import botocore.exceptions

def wait_for_status(client, get_fn, resource_id, *, timeout_s=300, interval_s=10):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            resp = get_fn(resource_id)
            if resp.get("status") == "READY":
                return resp
        except botocore.exceptions.ClientError as e:
            # expected operational failure; decide whether to retry/exit
            raise
        time.sleep(interval_s)
    raise TimeoutError(f"Timed out waiting for {resource_id} to become READY")

def create_and_poll(cp_client, *, state, create_fn, get_fn):
    # 1) create
    resp = create_fn()
    state["id"] = resp["id"]  # 2) persist immediately (idempotency for reruns)
    # 3) poll
    return wait_for_status(cp_client, get_fn, state["id"])

def parse_metadata(json_bytes):
    try:
        return json.loads(json_bytes)
    except json.JSONDecodeError:
        # expected corruption: degrade gracefully
        return {"events": [], "duration": 0}
```

Apply this standard especially to (1) retry/poll workflows and (2) external data sources (S3, APIs) where partial failure is expected.