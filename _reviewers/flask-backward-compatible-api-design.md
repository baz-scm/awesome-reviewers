---
title: Backward-compatible API design
description: When adding or changing public API surface, favor explicit, well-documented
  parameters over hidden `**kwargs` popping, and evolve signatures in a way that keeps
  existing behavior working.
repository: pallets/flask
label: API
language: Python
comments_count: 6
repository_stars: 75022
---

When adding or changing public API surface, favor explicit, well-documented parameters over hidden `**kwargs` popping, and evolve signatures in a way that keeps existing behavior working.

- Add new options as named parameters in the function signature (not via `options.pop(...)`) so they appear in the docstring and are discoverable, e.g. `provide_automatic_options` should be a real parameter of `add_url_rule`, not something silently popped out of `**options`.
- Avoid sentinel values that are ambiguous with "not provided". If `None` is a legitimate value (e.g. `json=None` meaning "send JSON null"), don't reuse it as "argument not passed"; instead detect presence via `"json" in kwargs` or a dedicated sentinel.
- When generalizing an existing API (e.g. turning `from_json(filename)` into a more flexible `from_file(filename, loads)`), keep the old method as a thin wrapper delegating to the new one, and mark it with a `DeprecationWarning` rather than removing or silently changing its behavior.
- Before adding new validation/assertions to existing public methods (e.g. asserting that a view function name contains no dots), verify they don't reject previously valid, supported usage (such as partials or custom endpoint names) — gate the check so it only applies when relevant.
- When composing nested/hierarchical options (such as blueprint `subdomain` and `url_prefix`), define and document a single, predictable combination rule (e.g., child values nest with parent values) instead of silently overriding or raising errors that would break legitimate configurations.

Example of safe evolution with deprecation:
```python
def from_file(self, filename, loads, silent=False):
    """Update config from a file loaded via `loads`."""
    ...
    return self.from_mapping(obj)

def from_json(self, filename, silent=False):
    """Deprecated: use from_file(filename, json.loads) instead."""
    warnings.warn(
        "'from_json' is deprecated and will be removed in 2.0. Use 'from_file' instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return self.from_file(filename, json.loads, silent=silent)
```

This keeps the public API stable for existing users while enabling richer, more flexible functionality going forward.