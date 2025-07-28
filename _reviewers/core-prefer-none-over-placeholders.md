---
title: prefer None over placeholders
description: When data is unavailable, unknown, or invalid, return `None` instead
  of placeholder strings like "Unknown", "Unspecified", or "???". This makes the absence
  of data explicit and prevents downstream code from treating placeholder values as
  legitimate data.
repository: home-assistant/core
label: Null Handling
language: Python
comments_count: 5
repository_stars: 80450
---

When data is unavailable, unknown, or invalid, return `None` instead of placeholder strings like "Unknown", "Unspecified", or "???". This makes the absence of data explicit and prevents downstream code from treating placeholder values as legitimate data.

**Apply this pattern when:**
- API responses contain unknown/invalid values that should be mapped to `None`
- Optional device attributes are missing and would otherwise get placeholder defaults
- Enum values are unrecognized and should be treated as missing rather than preserved as strings

**Example:**
```python
# Avoid placeholder defaults
model=host_data.get("devmodel")  # Returns None if missing
# Instead of:
model=host_data.get("devmodel", "Unknown")

# Map invalid values to None
return {"???": None, "UNSPECIFIED": None}.get(raw_value, raw_value)
# Instead of:
return {"???": "unknown"}.get(raw_value, raw_value)
```

**Always pair with null checks:**
```python
if self._device.data["_state"]["lastComms"] is not None:
    self._last_comms = dt_util.utc_from_timestamp(
        self._device.data["_state"]["lastComms"]
    )
```

This approach makes data availability explicit, prevents confusion between actual values and placeholders, and enables proper null safety patterns throughout the codebase.