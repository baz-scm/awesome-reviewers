---
title: Clean typing and DRY
description: 'Adopt a “type-correct, DRY, and clean” coding style.


  Rules:

  1) Make type hints compile and be precise

  - If you use `Dict`, `List`, `Union`, etc., import them from `typing` (or use built-in
  `dict`/`list` where appropriate).'
repository: eosphoros-ai/DB-GPT
label: Code Style
language: Python
comments_count: 7
repository_stars: 18703
---

Adopt a “type-correct, DRY, and clean” coding style.

Rules:
1) Make type hints compile and be precise
- If you use `Dict`, `List`, `Union`, etc., import them from `typing` (or use built-in `dict`/`list` where appropriate).
- Initialize typed containers explicitly (e.g., `intention: Dict[str, Union[str, List[str]]] = {}`) to avoid ambiguous types.

2) Remove unused assignments and dead code
- Don’t keep variables that are never used; don’t leave commented-out behavior in committed code—fix properly or remove.

3) Avoid redundant abstractions/config branches
- Don’t add wrapper classes when the base type already covers the functionality.
- Don’t redeclare abstract methods in a subclass if they’re already declared in the parent.
- Centralize config flags once (e.g., read from config/getter) and branch using that single value.

Example (typing + unused-code cleanup):
```python
from typing import Dict, List, Union

def parse_intent(text: str) -> Dict[str, Union[str, List[str]]]:
    intention: Dict[str, Union[str, List[str]]] = {}  # typed and initialized
    # ... parse JSON, fill intention ...
    return intention
```

Example (DRY via config flag):
```python
def explore(..., graph_store):
    similarity_search_enabled = graph_store.get_config().similarity_search_enabled
    if similarity_search_enabled:
        # do embedding/search logic
        pass
    # else: fall through
```

Enforce these checks in review and via tooling (lint/type checker) so style remains consistent and code stays maintainable.