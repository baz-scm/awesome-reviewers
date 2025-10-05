---
title: Be specific with exceptions
description: Avoid catching broad exception types like `Exception` and instead catch
  specific exceptions that you expect and can handle appropriately. When errors occur,
  they should be explicit rather than failing silently, and should include proper
  logging or re-raising when necessary.
repository: commaai/openpilot
label: Error Handling
language: Python
comments_count: 4
repository_stars: 58214
---

Avoid catching broad exception types like `Exception` and instead catch specific exceptions that you expect and can handle appropriately. When errors occur, they should be explicit rather than failing silently, and should include proper logging or re-raising when necessary.

**Key principles:**
- Catch specific exception types rather than using broad `except Exception:` clauses
- Don't let failures happen silently - add logging or explicit error handling
- Re-raise exceptions when you can't handle them properly
- Be explicit about what can fail and why

**Example of what to avoid:**
```python
try:
    last_parameters_msg.liveParameters.stiffnessFactor = last_parameters_dict['stiffnessFactor']
    params_reader.put("LiveParameters", last_parameters_msg.to_bytes())
except Exception:  # Too broad, fails silently
    pass
```

**Better approach:**
```python
try:
    last_parameters_msg.liveParameters.stiffnessFactor = last_parameters_dict['stiffnessFactor']
    params_reader.put("LiveParameters", last_parameters_msg.to_bytes())
except (json.JSONDecodeError, KeyError) as e:  # Specific exceptions
    cloudlog.warn(f"Failed to migrate cached params: {e}")
```

This approach makes code more maintainable by clearly documenting what can go wrong and ensuring failures are visible rather than hidden.