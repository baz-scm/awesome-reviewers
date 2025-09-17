---
title: Prefer exceptions over silent failures
description: Raise exceptions instead of returning None, logging warnings, or silently
  modifying values when encountering error conditions. This makes failures explicit
  and forces callers to handle error cases properly, improving code reliability and
  debugging experience.
repository: langgenius/dify
label: Error Handling
language: Python
comments_count: 6
repository_stars: 114231
---

Raise exceptions instead of returning None, logging warnings, or silently modifying values when encountering error conditions. This makes failures explicit and forces callers to handle error cases properly, improving code reliability and debugging experience.

**Why this matters:**
- Returning None forces every caller to check for null values, similar to error handling in Go
- Silent failures or logging-only approaches hide problems until they cause issues downstream
- Exceptions provide clear stack traces and force explicit error handling

**Apply this by:**
- Replace `return None` for missing resources with specific exceptions
- Use exceptions instead of logging warnings for validation failures  
- Avoid silently modifying invalid input values in validators

**Example:**
```python
# ❌ Avoid - silent failure
def update_schedule(session: Session, schedule_id: str, updates: dict) -> Optional[WorkflowSchedulePlan]:
    schedule = session.get(WorkflowSchedulePlan, schedule_id)
    if not schedule:
        return None  # Forces caller to check for None

# ✅ Prefer - explicit exception
def update_schedule(session: Session, schedule_id: str, updates: dict) -> WorkflowSchedulePlan:
    schedule = session.get(WorkflowSchedulePlan, schedule_id)
    if not schedule:
        raise ValueError(f"Schedule not found: {schedule_id}")
    # ... rest of implementation
```

**Exception:** Use None returns only when the absence of a value is a valid business case, not an error condition.