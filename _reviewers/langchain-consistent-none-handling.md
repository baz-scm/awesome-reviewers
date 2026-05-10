---
title: Consistent None Handling
description: When a value can be missing/null, reflect it in the type system and handle
  it explicitly at the boundary—never leak `None` into observable outputs (yields,
  dict keys, metadata, merged content) and don’t “paper over” missing invariants with
  synthetic placeholders.
repository: langchain-ai/langchain
label: Null Handling
language: Python
comments_count: 7
repository_stars: 136312
---

When a value can be missing/null, reflect it in the type system and handle it explicitly at the boundary—never leak `None` into observable outputs (yields, dict keys, metadata, merged content) and don’t “paper over” missing invariants with synthetic placeholders.

Practical rules:
1) Prefer `X | None = None` (or `Optional[X]`) over sentinel-literals like `Literal[False]` for optional callables.
2) Guard before writing/using: if something derived could be `None` (e.g., a dict key), check before assignment.
3) Ensure iterators/streaming never yield `None` as a valid element unless the type says so.
4) Keep semantic distinctions: e.g., treat `args=None` as “streaming in-progress” and `args={}` as “completed no-args” to avoid parsing/execution bugs.
5) If an invariant is violated (e.g., “an AIMessage must exist”), either raise a clear error or widen the function signature and make callers handle the missing case—don’t create dummy objects that hide the underlying state bug.

Example patterns:
```py
from typing import Callable

# 1) Optional callable
length_fn: Callable[[list[str]], list[int]] | None = None

# 2) Guard None-derived keys
header_key = splittable_headers.get("#" * depth)
if header_key is not None:
    current_chunk.metadata[header_key] = value

# 3) Avoid yielding None
first_chunk = await first_map_chunk_task
if first_chunk is not None:
    yield first_chunk

# 4) Preserve streaming vs final semantics
# args=None => not ready to execute; args={} => execute with no args
if tool_call_args is None:
    # streaming/in-progress
    pass
else:
    # final state
    run_tool_with(tool_call_args)

# 5) Missing invariant: raise or widen types (don’t fabricate)
if last_ai_message is None:
    raise ValueError("Expected at least one AIMessage in state")
```
