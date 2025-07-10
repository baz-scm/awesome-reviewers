---
title: Defensive null checking
description: Implement defensive null checking to prevent NoneType errors, KeyError,
  and IndexError exceptions. When accessing dictionaries, collections, or optional
  values, verify existence before use.
repository: getsentry/sentry
label: Null Handling
language: Python
comments_count: 5
repository_stars: 41297
---

Implement defensive null checking to prevent NoneType errors, KeyError, and IndexError exceptions. When accessing dictionaries, collections, or optional values, verify existence before use.

For dictionary access:
```python
# Unsafe - may raise KeyError:
message = event["data"]["payload"]["message"]

# Safe - uses default value if key missing:
message = event["data"]["payload"].get("message")
# With explicit default:
message = event["data"]["payload"].get("message", "Unknown")
```

For collections:
```python
# Unsafe - may raise IndexError:
first_item = my_list[0]

# Safe - check before access:
if isinstance(my_list, list) and my_list:
    first_item = my_list[0]
```

For optional attributes:
```python
# Unsafe - may raise AttributeError or work unexpectedly:
if self.project_ids:  # This passes if project_ids is empty list but fails if None
    result = process_data(self.project_ids)

# Safe - explicit type check:
if self.project_ids is not None:
    result = process_data(self.project_ids)
```

For inconsistent external data:
```python
# Defensive type handling:
timestamp_raw = event.get("timestamp_ms", 0)
if isinstance(timestamp_raw, str):
    try:
        dt = datetime.fromisoformat(timestamp_raw.replace("Z", "+00:00"))
        timestamp = dt.timestamp() * 1000  # Convert to milliseconds
    except (ValueError, AttributeError):
        timestamp = 0.0
else:
    timestamp = float(timestamp_raw)
```