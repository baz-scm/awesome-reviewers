---
title: Favor clarity over brevity
description: Always prioritize code readability and maintainability over concise but
  cryptic implementations. Extract repeated logic into well-named helper functions,
  use keyword-only arguments for clearer APIs, and structure complex string operations
  for better readability.
repository: pola-rs/polars
label: Code Style
language: Python
comments_count: 3
repository_stars: 34296
---

Always prioritize code readability and maintainability over concise but cryptic implementations. Extract repeated logic into well-named helper functions, use keyword-only arguments for clearer APIs, and structure complex string operations for better readability.

For repeated code:
```python
# Instead of this:
if engine == "auto" and get_engine_affinity() != "auto":
    engine = get_engine_affinity()

# Extract into a reusable function:
def _select_engine(engine: EngineType) -> EngineType:
    return get_engine_affinity() if engine == "auto" else engine

# Then use it:
engine = _select_engine(engine)
```

For clearer APIs, use keyword-only arguments:
```python
# Instead of this:
def from_buffer(self, dtype: PolarsDataType, endianness: Endianness = "little"):
    ...

# Prefer this:
def from_buffer(self, *, dtype: PolarsDataType, endianness: Endianness = "little"):
    ...
```

For complex string operations, prefer readable structures:
```python
# Instead of complex concatenation:
categories = (
    [",".join(f"{cat!r}" for cat in categories[:3])]
    + ["…"]
    + [",".join(f"{cat!r}" for cat in categories[-3:])]
)

# Use more readable structure:
categories = [
    ",".join(repr(cat) for cat in categories[:3]),
    "…",
    ",".join(repr(cat) for cat in categories[-3:]),
]
```