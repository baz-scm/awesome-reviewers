---
title: Capture broad exceptions
description: When using broad exception handlers like `except Exception:`, always
  capture and log the exception to avoid silent failures that are difficult to debug
  in production. Broad exception handling without proper error capture masks underlying
  issues and makes troubleshooting nearly impossible.
repository: PostHog/posthog
label: Error Handling
language: Python
comments_count: 4
repository_stars: 28460
---

When using broad exception handlers like `except Exception:`, always capture and log the exception to avoid silent failures that are difficult to debug in production. Broad exception handling without proper error capture masks underlying issues and makes troubleshooting nearly impossible.

**Bad:**
```python
try:
    verify_github_signature(request.body.decode("utf-8"), kid, sig)
except Exception:
    # Silent failure - no way to debug what went wrong
    break
```

**Good:**
```python
try:
    verify_github_signature(request.body.decode("utf-8"), kid, sig)
except Exception as e:
    capture_exception(e)  # or logger.exception()
    break
```

This practice is especially critical in complex functions with nested operations where multiple failure points exist. Even when you intend to handle errors gracefully, capturing the exception provides valuable debugging information without changing the error handling behavior. The goal is to maintain your intended error recovery while ensuring production issues can be diagnosed and fixed.