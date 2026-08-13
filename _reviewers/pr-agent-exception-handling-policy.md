---
title: Exception Handling Policy
description: Adopt an exception-handling standard that distinguishes **critical control-flow**
  from **non-critical side effects**, while enforcing safe, observable exception patterns.
repository: the-pr-agent/pr-agent
label: Error Handling
language: Python
comments_count: 13
repository_stars: 12523
---

Adopt an exception-handling standard that distinguishes **critical control-flow** from **non-critical side effects**, while enforcing safe, observable exception patterns.

**1) Use framework-correct error propagation**
- In FastAPI/Starlette handlers, use `raise HTTPException(...)` (never `return HTTPException(...)`).

**2) Prefer specific exceptions where the library provides/uses distinct types**
- Catch the exceptions that actually occur (e.g., AWS IMDS flows: `BotoCoreError` *and* `ClientError`; OpenAI/LiteLLM retries: include timeout/connection types you want retried).
- For retry decorators or recovery paths, the exception tuple must match the real transient failures.

**3) For non-critical side effects, fail open—but document and log**
- Operations like “cleanup after update”, “load dedup markers”, “best-effort provider probes” must **never break publishing**.
- If you must use a broad `except`, keep it broad only in these fail-open zones, and **add a comment explaining why narrowing would be unsafe**.

**4) Re-raise correctly to preserve traceback**
- Prefer `raise` over `raise e` when rethrowing.

**5) Don’t use bare/empty catches**
- Avoid `except:` and avoid empty `except` blocks.
- If a catch is intentionally ignored, at least log (or include structured artifacts) explaining the degraded behavior.

**6) Make errors observable and stable**
- Log with context; when relevant, attach error details via structured artifacts instead of embedding unstable exception formatting.
- Don’t assume env vars are always present—guard and wrap file/env-dependent code in try/except.

**Example (safe fail-open cleanup + correct re-raise + framework raise)**
```python
from fastapi import HTTPException
from pr_agent.log import get_logger

def handler():
    # framework boundary: must raise
    raise HTTPException(status_code=503, detail="Service unavailable")

def best_effort_cleanup(git_provider, comment_url, cleanup_fn):
    # non-critical side effect: fail-open
    try:
        cleanup_fn()
    except Exception as cleanup_error:
        get_logger().warning(
            f"Cleanup failed for {comment_url}; continuing. error={cleanup_error}"
        )

def retryable_call():
    try:
        do_request()
    except KnownTransientError:
        raise  # allow retry framework to handle
    except Exception:
        get_logger().exception("Unexpected error; not retrying")
        raise
```

**When to broaden exceptions**: only for explicitly fail-open side effects (dedup loads, cleanup, best-effort provider operations). Otherwise, narrow to specific, meaningful exceptions and re-raise properly when you must abort.