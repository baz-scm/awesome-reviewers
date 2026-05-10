---
title: Test Canvas Edge Cases
description: 'When changing Celery task dispatch semantics (especially Canvas: chains/groups/chords,
  unroll/freeze, and composed workflows), add regression tests that:'
repository: celery/celery
label: Celery
language: Python
comments_count: 4
repository_stars: 28464
---

When changing Celery task dispatch semantics (especially Canvas: chains/groups/chords, unroll/freeze, and composed workflows), add regression tests that:

- Cover edge/no-op compositions (e.g., empty/effectively-empty chains inside headers) to ensure they’re skipped and don’t hang.
- Verify propagation of configured behavior across all primitives (e.g., a single `task_id_generator` used consistently throughout a canvas workflow).
- Assert real execution/behavior, not only “no exception” (e.g., patch `apply_async` and confirm only intended tasks/bodies are applied).
- Validate result metadata/stamping for nested compositions and replacements (e.g., group stamps are stored in the correct order and aren’t lost due to `replaced`).

Example pattern for asserting the executed path (empty-chain chord header):

```python
# chord whose header contains only empty chains should not apply header tasks
from celery import chord, group, chain

# header member is effectively empty
empty_chain_sig = chain(tuple())
child_count = 24
child_chord = chord([empty_chain_sig], body=add.si(0, 0))
header = group([child_chord] * child_count)

# patch Signature.apply_async and assert only chord bodies run
header.apply_async()
assert mock_apply_async.call_count == child_count
```

Apply this same approach when testing task-id generation and metadata stamping: freeze signatures, run the canvas workflow, and assert the expected `task_id` source and `_get_task_meta()` contents for each composed element.