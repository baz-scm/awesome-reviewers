---
title: Assert the targeted change
description: 'Many tests in this codebase verify overall end-to-end success without
  ever asserting the specific invariant that the change was meant to guard. A test
  that only checks final output can keep passing even if the actual fix regresses,
  or can pass vacuously (e.g., looping over a result that happens to be empty). When
  writing or reviewing a test:'
repository: kyegomez/swarms#pi240310
label: Testing
language: Python
comments_count: 9
repository_stars: 7337
---

Many tests in this codebase verify overall end-to-end success without ever asserting the specific invariant that the change was meant to guard. A test that only checks final output can keep passing even if the actual fix regresses, or can pass vacuously (e.g., looping over a result that happens to be empty). When writing or reviewing a test:

1. Identify the precise behavior the change introduces or fixes, and add a direct assertion on it (e.g., assert `agent.output_type == "final"` rather than only checking the final answer; assert `_read_shared_state()` still round-trips the audit log if that path remains load-bearing).
2. Exercise the code path that was actually modified, using real construction (`Agent(...)` through `__init__`) rather than bypassing initialization, when the claim concerns default/real-object behavior.
3. Cover the branch that matters most for the semantic change, not just the easiest/first-call case (e.g., also test "failure after some output already recorded," not only "failure on the very first call").
4. Guard against vacuously-true assertions: if a test asserts properties of items in a collection, first assert the collection is non-empty.

```python
for call in calls:
    assert isinstance(call["messages"], list)
    assert call["messages"], f"{call['agent']} got no turns"  # guard against vacuous pass
    for message in call["messages"]:
        ...
```

5. When indexing into a result that could legitimately be empty on regression, assert non-emptiness first so failures report clearly instead of raising an unrelated `IndexError`.
6. If a naming or coverage gap between two parallel tests is intentional, say so in a comment; otherwise close the gap so both cases assert the same invariants.

Applying this standard ensures tests fail for the right reason when the guarded behavior regresses, rather than passing by coincidence or failing with an unrelated/confusing error.