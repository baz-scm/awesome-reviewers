---
title: Lock Writes, Snapshot Reads
description: 'Use the lock to protect shared mutable state during mutations, but avoid
  holding it for read-side convenience/field-by-field getters.


  **Rules**

  1. **Lock only for writes:** Acquire the mutex only around code that mutates shared
  collections/fields (e.g., `logs[]`, `updates[]`, `notifications[]`).'
repository: agent0ai/agent-zero
label: Concurrency
language: Python
comments_count: 3
repository_stars: 17612
---

Use the lock to protect shared mutable state during mutations, but avoid holding it for read-side convenience/field-by-field getters.

**Rules**
1. **Lock only for writes:** Acquire the mutex only around code that mutates shared collections/fields (e.g., `logs[]`, `updates[]`, `notifications[]`).
2. **Minimize critical sections:** Do expensive or deterministic work (masking, truncation, formatting) *outside* the lock; lock only to commit the final updates.
3. **Reads: prefer no lock or atomic snapshots:**
   - If your read is “best-effort” and does not require a logically consistent multi-field view, avoid locking.
   - If you need a consistent snapshot across multiple related reads, either:
     - lock the whole read sequence, or
     - copy the needed data under lock, then release and compute/iterate outside.

**Example pattern (commit under lock, transform outside)**
```python
def update_item(self, *, no: int, heading: str | None, content: str | None):
    # Preprocess outside the lock
    if heading is not None:
        new_heading = _truncate_heading(self._mask_recursive(heading))
    if content is not None:
        item_type = self.logs[no].type  # or pass in required type explicitly
        new_content = _truncate_content(self._mask_recursive(content), item_type)

    with self._lock:
        item = self.logs[no]
        if heading is not None:
            item.heading = new_heading
        if content is not None:
            item.content = new_content
        self.updates.append(item.no)
```

Applying this standard will reduce lock contention, prevent unnecessary refactors tied to read-side locking, and still keep shared writes thread-safe.