---
title: Semantic, convention-compliant identifiers
description: Choose identifier names (variables, parameters, functions, env vars)
  that precisely describe what they represent or do, and keep them in sync when behavior
  changes. Follow the language's naming conventions (e.g. PEP8 snake_case in Python,
  never camelCase for functions/variables). Avoid names that are misleading, inverted
  in meaning, or reused for a...
repository: pallets/flask#x
label: Naming Conventions
language: Python
comments_count: 6
repository_stars: 75163
---

Choose identifier names (variables, parameters, functions, env vars) that precisely describe what they represent or do, and keep them in sync when behavior changes. Follow the language's naming conventions (e.g. PEP8 snake_case in Python, never camelCase for functions/variables). Avoid names that are misleading, inverted in meaning, or reused for a different purpose than their origin suggests.

Examples of what to avoid and fix:
- A parameter named `text=True` that actually forces binary mode should be renamed to something like `binary=True` so its name matches its effect.
- A helper renamed/generalized internally (e.g. `update` that now also calls `ensure_sync`) but keeps a generic name should get a more specific name reflecting its new, non-generic behavior.
- Don't shadow a variable name with a value of a different type/meaning than what it will later be used for, e.g.:
  ```python
  # Bad: `load_dotenv` is also the name of a function called later
  val = os.environ.get("FLASK_DONT_LOAD_ENV")
  load_dotenv = not val or val in ("0", "false", "no")
  ...
  load_dotenv(...)  # confusing: name now means two different things
  ```
  Use a distinct name like `should_load_dotenv` instead.
- Environment variables and constants should be named to unambiguously convey their scope/trigger, e.g. prefer `FLASK_RUN_CLI_FROM_APP_RUN` over the ambiguous `FLASK_RUN_FROM_APP_RUN`.
- Never use camelCase for Python functions (e.g. `_isAdHoc`) — use `snake_case` (`_is_adhoc`), and avoid introducing indirection/function calls for simple conditions that don't add clarity.

When adding or changing a parameter, variable, or function, double-check the name still accurately and unambiguously describes its current purpose, and matches established naming style for the surrounding codebase/language.