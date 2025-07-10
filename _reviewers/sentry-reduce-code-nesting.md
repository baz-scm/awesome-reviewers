---
title: Reduce code nesting
description: 'Excessive indentation makes code harder to read and understand. Two
  common techniques can help flatten your code structure:


  1. **Use early returns** for guard conditions instead of nesting the main logic
  in else blocks:'
repository: getsentry/sentry
label: Code Style
language: Python
comments_count: 2
repository_stars: 41297
---

Excessive indentation makes code harder to read and understand. Two common techniques can help flatten your code structure:

1. **Use early returns** for guard conditions instead of nesting the main logic in else blocks:

```python
# Instead of this:
def increment_group_tombstone_hit_counter(tombstone_id: int | None, event: Event) -> None:
    if tombstone_id:
        # deeply nested logic here
        # ...

# Prefer this:
def increment_group_tombstone_hit_counter(tombstone_id: int | None, event: Event) -> None:
    if not tombstone_id:
        return
    
    # main logic here at the top level
    # ...
```

2. **Use compound context managers** to reduce indentation levels when multiple contexts are needed:

```python
# Instead of this:
with mock.patch(...):
    with self.feature(...):
        with self.tasks():
            with pytest.raises(...):
                # deeply nested code

# Prefer this:
with (
    mock.patch(...),
    self.feature(...),
    self.tasks(),
    pytest.raises(...)
):
    # code at a more readable indentation level
```

These techniques produce flatter, more scannable code that's easier to maintain and debug. This pattern is sometimes called "flattening arrow code" as it helps avoid the rightward drift that can make functions hard to follow.