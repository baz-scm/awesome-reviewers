---
title: Raise contextual error types
description: Always raise specific, contextual exception types instead of generic
  exceptions. Include relevant error details that help identify the root cause and
  potential solutions. This improves error tracking, debugging, and system reliability.
repository: getsentry/sentry
label: Error Handling
language: Python
comments_count: 4
repository_stars: 41297
---

Always raise specific, contextual exception types instead of generic exceptions. Include relevant error details that help identify the root cause and potential solutions. This improves error tracking, debugging, and system reliability.

Bad:
```python
if response.status_code != 200:
    raise Exception("A non 200 HTTP status code was returned.")

if not data:
    raise Exception("Invalid response from LLM")
```

Good:
```python
if response.status_code != 200:
    raise ValueError(
        f"Seer API returned unexpected status code {response.status_code}: {response.text}"
    )

if not data:
    raise ValueError("LLM returned empty response when generating summary")
```

The specific exception type (e.g., ValueError, TypeError, KeyError) should match the error condition. Include relevant context like parameter values, system state, or error messages in the exception text. This helps with:
- Faster debugging through better error attribution
- More accurate error tracking and aggregation
- Proper error handling by upstream code
- Clear documentation of failure modes