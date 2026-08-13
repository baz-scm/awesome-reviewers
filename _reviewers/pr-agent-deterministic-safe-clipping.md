---
title: Deterministic Safe Clipping
description: When collecting, deduplicating, and truncating algorithm outputs (e.g.,
  “top N” items, merged references, ranked suggestions), enforce determinism and configuration-consistent
  clipping.
repository: the-pr-agent/pr-agent
label: Algorithms
language: Python
comments_count: 4
repository_stars: 12523
---

When collecting, deduplicating, and truncating algorithm outputs (e.g., “top N” items, merged references, ranked suggestions), enforce determinism and configuration-consistent clipping.

Rules:
1) Never truncate by slicing an unordered container.
- If you use a `set` for deduplication, do not slice it directly (hash iteration order is nondeterministic).
- Instead: keep a separate ordered list (first-seen order) and dedupe by membership.

2) Make clipping logic configuration-aware and intent-preserving.
- If the system has minimum/priority expectations (e.g., “always keep at least one from source X” or “don’t reduce below what config implies”), encode that explicitly rather than relying on a generic factor (like `final_clip_factor`) to halve results.

3) Prefer bounded iteration over recursion for repair loops.
- If you repeatedly attempt to fix/parse malformed content (JSON/YAML/etc.), use a `while` loop with a max-iteration/termination condition rather than recursion.

Example (ordered dedupe + safe truncation with mixed-source intent):
```python
MAX_TICKETS = 3

def merge_and_truncate(github_like_links, asana_links, max_tickets=MAX_TICKETS):
    seen = set()
    merged = []

    def add_links(links):
        for link in links:
            if link not in seen:
                seen.add(link)
                merged.append(link)

    # Deterministic: use input order (first-seen order)
    # Intent-preserving: reserve at least one slot for Asana if present
    github_like_links = list(github_like_links)
    asana_links = list(asana_links)

    reserved_for_asana = 1 if asana_links else 0
    add_links(github_like_links[: max_tickets - reserved_for_asana])
    add_links(asana_links[: reserved_for_asana])

    return merged[:max_tickets]
```

Example (bounded iterative JSON repair):
```python
import json

def fix_json_message(json_message, max_iter=10):
    for _ in range(max_iter):
        try:
            return json.loads(json_message)
        except Exception:
            # apply one corrective step to json_message
            # (e.g., replace offending char at computed index)
            # then continue
            pass
    return {}
```

Adopting these rules prevents flaky behavior in production (nondeterministic truncation), avoids surprising drops relative to configuration intent, and keeps “repair” algorithms safe from stack overflows or runaway recursion.