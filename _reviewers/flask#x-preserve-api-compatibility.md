---
title: Preserve API compatibility
description: When adding or changing behavior of a public method, do not break existing
  call signatures, documented arguments, or expected semantics. New options should
  be added as explicit, documented parameters (not silently popped from `**options`/`**kwargs`),
  so they show up in the function signature and docstring and can be discovered by
  users and tools. Defaults...
repository: pallets/flask#x
label: API
language: Python
comments_count: 7
repository_stars: 75163
---

When adding or changing behavior of a public method, do not break existing call signatures, documented arguments, or expected semantics. New options should be added as explicit, documented parameters (not silently popped from `**options`/`**kwargs`), so they show up in the function signature and docstring and can be discovered by users and tools. Defaults for new parameters must match prior behavior to avoid surprising reversals (e.g. a new `text` flag defaulting to the old text-mode behavior, not binary). If a function previously accepted certain positional/keyword arguments (such as `provide_automatic_options` or the URL rule args passed to `dispatch_request`), continued support for those arguments must be preserved even while refactoring internals.

When a feature composes with an existing one (e.g. blueprint `subdomain` nesting alongside `url_prefix` nesting), its behavior should follow the same, well-established pattern (combine/nest) rather than introducing an inconsistent or surprising rule, unless there is a strong, documented reason to diverge.

When replacing an old API with a more general one (e.g. `from_json` superseded by `from_file`), keep the old method working as a thin wrapper and mark it with a `DeprecationWarning` noting the version it will be removed in, rather than removing it outright.

Example of adding a new option correctly:
```python
def add_url_rule(
    self, rule, endpoint=None, view_func=None,
    provide_automatic_options=None, **options
):
    """
    :param provide_automatic_options: Add the default OPTIONS method.
    """
    ...
```
rather than:
```python
provide_automatic_options = options.pop("provide_automatic_options", ...)
```

Before merging an API change, verify: existing callers still work unmodified, new parameters are documented and discoverable, defaults preserve prior behavior, and any removed API path is deprecated rather than deleted.