---
title: Implement graceful error handling
description: Replace assertions, unhandled exceptions, and error-suppression mechanisms
  with proper error handling that provides clear, actionable feedback to users. Instead
  of allowing applications to crash or silently hide issues, implement structured
  error handling that communicates what went wrong and suggests next steps.
repository: emcie-co/parlant
label: Error Handling
language: Other
comments_count: 2
repository_stars: 12205
---

Replace assertions, unhandled exceptions, and error-suppression mechanisms with proper error handling that provides clear, actionable feedback to users. Instead of allowing applications to crash or silently hide issues, implement structured error handling that communicates what went wrong and suggests next steps.

For example, replace crash-prone assertions:
```python
# Avoid - can crash ungracefully
assert await params.indexer.index(container)

# Prefer - graceful handling with clear messaging
try:
    success = await params.indexer.index(container)
    if not success:
        raise RuntimeError("Failed to index container. Check your configuration and try again.")
except Exception as e:
    logger.error(f"Indexing failed: {e}")
    raise RuntimeError("Indexing operation failed. Please verify your setup and retry.") from e
```

Similarly, avoid broad error suppression (like blanket `ignore_missing_imports`) that can mask real issues. Handle specific error cases individually to maintain visibility into potential problems while still providing a good user experience.