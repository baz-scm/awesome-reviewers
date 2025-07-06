---
title: Use universally understandable identifiers
description: When naming variables, functions, routes, and other code elements, use
  clear, neutral terminology that will be understood by all developers regardless
  of their cultural or domain-specific knowledge. This is especially important in
  tests, examples, and documentation where context may not be obvious.
repository: fastapi/fastapi
label: Naming Conventions
language: Python
comments_count: 2
repository_stars: 86871
---

When naming variables, functions, routes, and other code elements, use clear, neutral terminology that will be understood by all developers regardless of their cultural or domain-specific knowledge. This is especially important in tests, examples, and documentation where context may not be obvious.

For test names, use descriptive identifiers that clearly indicate what's being tested, including test conditions and parameters:

```python
# Less clear:
def test_create_item():
    # ...

# More clear:
def test_create_item_when_separate_input_output_schemas_is():
    # ...
```

For route paths and other public-facing code, prefer neutral, generic terms over domain-specific or culturally-bound terminology:

```python
# Potentially confusing:
@app.get("/pita/shuli")
def get_pita_shuli():
    # ...

# Clearer for all developers:
@app.get("/category/item")
def get_category_item():
    # ...
```

Clear naming reduces the cognitive load for all developers interacting with the codebase, especially those who are new to the project or from different cultural backgrounds.