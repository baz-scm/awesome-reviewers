---
title: Cap retries, cache calls
description: 'For performance-critical code paths, prevent wasted work and unbounded
  waits: (1) fetch/cache expensive data once (e.g., registry lookups/credentials,
  repeated GETs) and pass it into helpers; (2) bound polling/retry time with explicit
  per-attempt and total worst-case limits; (3) add timeouts for slow infrastructure
  operations.'
repository: Azure/azure-cli
label: Performance Optimization
language: Python
comments_count: 4
repository_stars: 4592
---

For performance-critical code paths, prevent wasted work and unbounded waits: (1) fetch/cache expensive data once (e.g., registry lookups/credentials, repeated GETs) and pass it into helpers; (2) bound polling/retry time with explicit per-attempt and total worst-case limits; (3) add timeouts for slow infrastructure operations.

Application checklist:
- Network/API calls: do not call the same “get”/lookup multiple times in separate helpers—retrieve once at the top-level and thread the result through.
- Retries/polling: implement exponential backoff with a capped per-attempt sleep and a configured max-delay/max-retries so the runner’s worst-case runtime is bounded.
- IO/module loading: apply a timeout for potentially long operations; validate against observed p99 latency and choose a safe default.

Example (bounded backoff + fetch-once pattern):
```python
import os, random, time

def run_check(cmd, request_id, checks):
    # Fetch once (e.g., registry, creds, client data)
    registry, creds = fetch_registry_and_creds_once(cmd, request_id)

    max_retries = max(1, int(os.environ.get('MAX_RETRIES', '10')))
    base_delay = float(os.environ.get('BASE_DELAY', '2.0'))
    max_delay = float(os.environ.get('MAX_DELAY', '60.0'))  # cap per-attempt

    for attempt in range(max_retries):
        result = execute_check(cmd, registry, creds, checks)
        if is_terminal(result):
            return result

        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
        time.sleep(min(delay, max_delay))

    raise TimeoutError("Retry budget exhausted")
```
