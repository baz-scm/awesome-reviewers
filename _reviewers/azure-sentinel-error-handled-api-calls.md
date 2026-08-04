---
title: Error-handled API Calls
description: 'For every external API/data-store call, enforce a consistent error-handling
  contract:


  1) Validate inputs up front (fail fast for predictable bad requests)'
repository: Azure/Azure-Sentinel
label: Error Handling
language: Python
comments_count: 5
repository_stars: 6042
---

For every external API/data-store call, enforce a consistent error-handling contract:

1) Validate inputs up front (fail fast for predictable bad requests)
- Example: if the computed window is invalid, skip/exit instead of calling the API.

2) Wrap the call in try/catch and log with traceback
- Use `logging.exception(...)` (or equivalent) inside the except block so you keep the stack trace.
- If you rethrow, prefer bare `raise` to preserve the original stack.

3) Retry only transient failures with status-aware logic
- Retry on transient responses such as HTTP 429 and 5xx (e.g., 500/502/503/504).
- Do not retry on non-transient/auth/client errors (e.g., 400/401); instead log a clear message and exit (or degrade gracefully).

4) Make retry termination explicit
- Use a max-attempts counter/backoff and stop once exceeded.

Self-contained example (pattern to follow):
```python
import logging
import time
import requests

TRANSIENT_STATUS = {429, 500, 502, 503, 504}

def call_with_retries(url, headers, params, max_retries=3, backoff_seconds=1):
    if params.get("from") and params.get("to") and params["from"] >= params["to"]:
        logging.info("Skipping call due to invalid time window")
        return None

    attempt = 0
    while True:
        try:
            resp = requests.get(url, headers=headers, params=params)
            if resp.status_code in TRANSIENT_STATUS:
                attempt += 1
                if attempt > max_retries:
                    logging.error(f"Exceeded retries for transient status {resp.status_code}")
                    return None
                time.sleep(backoff_seconds * attempt)
                continue

            if resp.status_code in {400, 401}:
                logging.error(f"Non-retryable API error {resp.status_code}: {resp.text}")
                return None

            resp.raise_for_status()
            return resp.json()

        except Exception:
            logging.exception("API call failed")
            attempt += 1
            if attempt > max_retries:
                raise
            time.sleep(backoff_seconds * attempt)
```
Apply this pattern consistently so failures are recoverable when appropriate, non-retryable errors don’t waste attempts, and logs/stack traces remain diagnosable.