---
title: Use Clear Style Helpers
description: 'Adopt maintainable, idiomatic Python patterns to improve readability
  and reduce future change risk.


  ### 1) Prefer `isinstance()` over `type(...) == ...`'
repository: the-pr-agent/pr-agent
label: Code Style
language: Python
comments_count: 8
repository_stars: 12523
---

Adopt maintainable, idiomatic Python patterns to improve readability and reduce future change risk.

### 1) Prefer `isinstance()` over `type(...) == ...`
Use idiomatic checks and keep conversions explicit.
```py
pr_types = []
if 'PR Type' in data:
    val = data['PR Type']
    pr_types = val if isinstance(val, list) else val.split(',')
```

### 2) Never use mutable values as default arguments
Use `None` and initialize inside the function.
```py
def try_fix_yaml(response_text: str, keys_fix_yaml: list[str] | None = None) -> dict:
    keys_fix_yaml = keys_fix_yaml or []
    ...
```

### 3) Extract validation/branch-heavy logic into helpers
Keep public/entry methods short and readable by moving validation into `is_valid_*` functions.
```py
def publish_code_suggestions(self, code_suggestions: list[dict]):
    for suggestion in code_suggestions:
        if not self.is_valid_suggestion(suggestion):
            continue
        ...

def is_valid_suggestion(self, suggestion: dict) -> bool:
    start = suggestion['relevant_lines_start']
    end = suggestion['relevant_lines_end']
    if (not start) or start == -1:
        return False
    return end >= start
```

### 4) Keep interfaces clean; reduce complexity
- If a function grows large, encapsulate parameters (e.g., a `Params` dataclass) instead of long signatures.
- Avoid deep if/else chains for command routing; prefer a dict mapping action→handler.

These rules directly support the discussed improvements in typing correctness, safe defaults, readability, and maintainability—core concerns for code style.