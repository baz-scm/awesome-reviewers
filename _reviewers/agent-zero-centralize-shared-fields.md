---
title: Centralize shared fields
description: When multiple modules need the same state/config/schema (e.g., context
  variables like timezone, or prompt search paths), do not replicate those fields
  or the logic that derives them in several places. Instead, funnel access through
  a single abstraction and reuse shared utilities.
repository: agent0ai/agent-zero
label: Code Style
language: Python
comments_count: 4
repository_stars: 17612
---

When multiple modules need the same state/config/schema (e.g., context variables like timezone, or prompt search paths), do not replicate those fields or the logic that derives them in several places. Instead, funnel access through a single abstraction and reuse shared utilities.

How to apply:
- Single source of truth: If snapshot/state is the canonical model, expose typed getters/builders (or pass around the snapshot-derived object) so handlers/schedulers don’t individually parse/maintain each field.
- Centralize composition logic: Put “include plugins” (or similar discovery rules) into one shared helper (e.g., `subagents.get_paths(..., include_plugins=True)`) instead of building paths in multiple call sites.
- Small readability refactors: Prefer extracting complex expressions/branches into named variables for clarity (especially around error handling/cleanup).

Example (pattern):
```python
# Instead of each module reading/handling timezone separately,
# make snapshot the source of truth.

# snapshot.py
@dataclass
class SnapshotContext:
    timezone: str
    # ...other shared fields

def build_context_from_snapshot(snapshot: Any) -> SnapshotContext:
    return SnapshotContext(timezone=snapshot.timezone)

# state_sync_handler.py
ctx = build_context_from_snapshot(snapshot)
state_monitor.mark_dirty(sid, reason=reason, timezone=ctx.timezone)

# Or, if StateMonitor only stores projection fields,
# accept an object built from snapshot rather than individual scalars.
```

This reduces “adjust multiple scripts when fields change” and keeps code organization consistent while improving readability.