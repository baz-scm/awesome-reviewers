---
title: PEP8-compliant, semantically accurate naming
description: 'All identifiers (functions, variables, parameters, methods) must follow
  PEP8 casing rules and clearly reflect what they actually represent or do. Specifically:'
repository: pallets/flask
label: Naming Conventions
language: Python
comments_count: 6
repository_stars: 75022
---

All identifiers (functions, variables, parameters, methods) must follow PEP8 casing rules and clearly reflect what they actually represent or do. Specifically:

- Use `snake_case` for functions and variables, never `camelCase`. For example, `_isAdHoc` should be `_is_adhoc`, and `is_IP` should be `is_ip`.
- Choose names that match the real behavior/type of the value, not a misleading or unrelated concept. A parameter named `text` that actually switches to binary mode should instead be named something like `binary`, matching the semantics of `open()`'s mode flag. Likewise, a function named `is_ip` that also validates input and raises/formats errors should be renamed to reflect that broader responsibility (e.g., `validate_ip`), rather than implying a simple boolean check.
- Never shadow a meaningfully-named function/method with a local variable of a different type/purpose. For instance, avoid:
  ```python
  val = os.environ.get('FLASK_DONT_LOAD_ENV')
  load_dotenv = not val or val in ('0', 'false', 'no')  # bool now shadows the load_dotenv() function
  ```
  Instead use a distinct name such as `should_load_dotenv` to avoid confusing readers about whether `load_dotenv` refers to the callable or a flag.
- Follow Python convention and name the first parameter of instance methods `self` (not `req` or other domain-specific names), even when refactoring from a standalone function into a method.

Apply these checks during review: confirm casing matches PEP8, confirm the name accurately conveys the identifier's purpose/type, and confirm no naming collisions or shadowing occur between variables and existing functions/methods.