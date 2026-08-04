---
title: Async status over loops
description: When using AgentCore Runtime for long-running/async jobs, manage concurrency
  by relying on the runtime’s status mechanisms rather than blocking or implementing
  unbounded wait loops. Clients should start the async job, return immediately, and
  then use the provided status API/methods or the /ping health signal to determine
  progress.
repository: awslabs/agentcore-samples
label: Concurrency
language: Other
comments_count: 2
repository_stars: 3244
---

When using AgentCore Runtime for long-running/async jobs, manage concurrency by relying on the runtime’s status mechanisms rather than blocking or implementing unbounded wait loops. Clients should start the async job, return immediately, and then use the provided status API/methods or the /ping health signal to determine progress.

Apply this standard:
- Start the async job and don’t block the request thread/process waiting for completion.
- Use the runtime’s status method (e.g., `job.status()` / equivalent) to check completion instead of `while True: sleep(...)` polling.
- Treat `/ping` responses like `{"status": "HealthyBusy"}` as “service healthy but busy/in-progress,” and continue status checks rather than assuming an error.
- Update tutorial/docs to explicitly describe the async job flow and the meaning of status values (including `HealthyBusy`) so consumers implement correct backoff/continuation behavior.

Example pattern (pseudo-Python):
```python
# 1) Kick off async work (returns quickly)
job = runtime.start_async_job(payload)

# 2) Check job state using runtime status (avoid manual tight loops)
while True:
    st = job.status()  # runtime-provided status call
    if st in ("SUCCEEDED", "FAILED"):
        break
    # Optional: sleep/backoff to reduce load
    time.sleep(1)

# 3) If applicable, also interpret /ping
# if ping returns {"status": "HealthyBusy"}, treat as in-progress.
```