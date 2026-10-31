---
title: Explicit None checks
description: Always test for absence of a value with `is None` / `is not None` rather
  than truthiness or `== None`/`!= None`. Truthy checks silently misclassify valid-but-falsy
  values (0, "", {}, []) as missing, and `== None` is non-idiomatic and slower due
  to implicit bool conversion. This is especially important when building fallback
  chains with `or`, since `a or b`...
repository: pallets/flask
label: Null Handling
language: Python
comments_count: 8
repository_stars: 75022
---

Always test for absence of a value with `is None` / `is not None` rather than truthiness or `== None`/`!= None`. Truthy checks silently misclassify valid-but-falsy values (0, "", {}, []) as missing, and `== None` is non-idiomatic and slower due to implicit bool conversion. This is especially important when building fallback chains with `or`, since `a or b` will skip `a` even when it is a legitimate falsy value (e.g. port 0, an empty JSON body, or an empty string that should stay empty rather than become `None`). When chaining multiple optional sources, prefer an explicit filter such as `next((v for v in (a, b, default) if v is not None), default)` instead of `a or b or default`, and add tests covering the falsy-but-valid case (e.g. port `0`).

Also ensure variables that may remain unset are always given an explicit default. For example, don't rely on an `except ... as err:` binding surviving past the `except` block (Python clears it), and don't assume a helper variable (like `sn_host` from `server_name.partition(':')`) is defined when its source is `None` — initialize defaults before the conditional so every code path has a defined value.

Example:
```python
# Bad: treats {} and 0 as "missing"
if json:
    ...
if domain != None:
    ...
subdomain = self.url_map.default_subdomain or None if not self.subdomain_matching else None

# Good: explicit None checks, defaults set up front
if json is not None:
    ...
if domain is not None:
    ...
host = host or sn_host or default_host
port = int(next((p for p in (port, sn_port) if p is not None), default_port))
```