---
title: Readable formatting and idioms
description: Prioritize readability through consistent formatting and modern, simple
  idioms. For code style changes, ensure multiline constructs are formatted cleanly,
  complex conditions are made understandable (via extracted “effective” variables
  or small helpers), repeated patterns are factored out, and modern Python conventions
  are used.
repository: celery/celery
label: Code Style
language: Python
comments_count: 12
repository_stars: 28464
---

Prioritize readability through consistent formatting and modern, simple idioms. For code style changes, ensure multiline constructs are formatted cleanly, complex conditions are made understandable (via extracted “effective” variables or small helpers), repeated patterns are factored out, and modern Python conventions are used.

Apply these practices:
- Multiline constants/expressions: use parenthesized forms with correct line breaks; avoid unnecessary trailing `strip()` on multiline literals.
- Replace verbose list-building with comprehensions when building a list from an iterable.
- Complex conditionals: compute “effective” values first, then use a simple predicate.
- Repeated logic: extract a helper instead of duplicating the same loop/merge pattern.
- Use modern idioms: prefer `{}` for dict literals, `{**d1, **d2}` for dict merges, and keep imports ordered (isort).
- If you touch typing/style around special methods, ensure the change is correct (don’t add annotations or decorators that contradict Python semantics or future type-checking).

Example (multiline constant + readable conditional):

```python
MAP_ROUTES_MUST_BE_A_DICTIONORY = (
    "Starting from Celery 5.1 the task_routes configuration must be a dictionary. "
    "Support for providing a list of router objects will be removed in 6.0."
)

effective_exchange = exchange or queue_exchange_name
effective_rkey = routing_key or queue_exchange_routing_key
if not effective_exchange and not effective_rkey and exchange_type == "direct":
    # ...
    pass
```

When unsure, prefer the version that is easiest to scan in a code review: small helpers/variables, clear indentation, and minimal unnecessary transformations.