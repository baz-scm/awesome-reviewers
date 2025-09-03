---
title: Document implementation reasoning
description: Add comments that explain WHY implementation decisions were made, not
  just WHAT the code does. This is especially important for backwards compatibility
  hacks, workarounds, non-obvious logic checks, and temporary solutions.
repository: langflow-ai/langflow
label: Documentation
language: Python
comments_count: 2
repository_stars: 111046
---

Add comments that explain WHY implementation decisions were made, not just WHAT the code does. This is especially important for backwards compatibility hacks, workarounds, non-obvious logic checks, and temporary solutions.

For backwards compatibility measures, include:
- Date/version when introduced
- Reason for the compatibility requirement  
- Criteria for when it can be safely removed

For complex logic checks, explain the underlying business reason or technical constraint that necessitates the check.

Example:
```python
# Backwards compatibility hack introduced in v2.1.0 (Dec 2024)
# Maps old context_id system to new server-based sessions
# TODO: Remove after v3.0.0 when all clients migrate to new API
self._context_to_session: dict[str, tuple[str, str]] = {}

# Check if instance is Component subclass (but not Component itself)
# Required because we manually create Component instances from user dicts
# which need compilation/parsing, unlike pre-built Component classes
if isinstance(instance, type) and issubclass(instance, Component):
```

This practice helps future maintainers understand the codebase evolution and make informed decisions about refactoring or removing temporary measures.