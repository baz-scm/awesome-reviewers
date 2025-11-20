---
title: explicit null checks
description: 'Use explicit existence checks rather than value-based null checks, and
  be intentional about failing fast versus providing defaults for missing data.


  When checking for optional data, prefer checking for key/attribute existence rather
  than checking if values are truthy or greater than zero. This prevents subtle bugs
  where legitimate zero values or empty...'
repository: strands-agents/sdk-python
label: Null Handling
language: Python
comments_count: 5
repository_stars: 4044
---

Use explicit existence checks rather than value-based null checks, and be intentional about failing fast versus providing defaults for missing data.

When checking for optional data, prefer checking for key/attribute existence rather than checking if values are truthy or greater than zero. This prevents subtle bugs where legitimate zero values or empty strings are treated as missing data.

For missing required data, prefer explicit KeyError/AttributeError over None-based error handling to provide clearer error messages and fail fast.

**Prefer explicit existence checks:**
```python
# Good - check if key exists
if "cacheReadInputTokens" in usage:
    attributes["cache_read_tokens"] = usage["cacheReadInputTokens"]

# Avoid - value-based check that excludes valid zero values  
if usage.get("cacheReadInputTokens", 0) > 0:
    attributes["cache_read_tokens"] = usage["cacheReadInputTokens"]
```

**Fail fast for required data:**
```python
# Good - explicit KeyError for missing required field
status=Status(data["status"])

# Avoid - None handling that masks the real issue
status=Status(data.get("status"))  # Will fail with confusing None error
```

**Be intentional about defaults:**
```python
# Good - explicit defaults for optional fields with clear intent
usage = Usage(**{"inputTokens": 0, "outputTokens": 0, "totalTokens": 0, **event.get("usage", {})})

# Consider defensive checks only when inheritance/overrides make them necessary
if not hasattr(self, "session_type"):
    self.session_type = SessionType.AGENT
```