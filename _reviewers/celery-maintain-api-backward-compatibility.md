---
title: Maintain API Backward Compatibility
description: 'When changing code that affects a public interface (method signatures,
  CLI command arguments, plugin discovery, type/subscriptable behavior), treat it
  as an API contract: keep existing call patterns working, and ensure runtime semantics
  match the intended contract.'
repository: celery/celery
label: API
language: Python
comments_count: 5
repository_stars: 28464
---

When changing code that affects a public interface (method signatures, CLI command arguments, plugin discovery, type/subscriptable behavior), treat it as an API contract: keep existing call patterns working, and ensure runtime semantics match the intended contract.

Practical rules:
- Preserve method/function signatures for externally-called APIs. If you need to change behavior, do it inside the body and/or accept/ignore parameters rather than removing them.
- For new parameters/CLI shapes, explicitly define and implement the parsing rules (including list/dict-like variants) and add tests for those input forms.
- For “interface-like” runtime behaviors (e.g., `__class_getitem__` / subscripting), ensure the runtime object you return matches the expected semantics (e.g., `types.GenericAlias`) and add a small runtime test.
- When behavior depends on Python/library versions (plugins, stdlib helpers), implement compatibility shims and test the relevant branches.

Example (signature stability):
```python
class EagerResult:
    # Keep legacy parameters in the signature even if the internal behavior no longer needs them.
    def get(self, timeout=None, propagate=True, disable_sync_subtasks=True, **kwargs):
        if self.successful():
            return self.result
        if self.state in states.PROPAGATE_STATES:
            if propagate:
                raise self.result if isinstance(self.result, Exception) else Exception(self.result)
            return self.result
```

Example (CLI input contract parsing):
```python
def revoke_by_stamped_header(state, header, terminate=False, signal=None, **kwargs):
    # Support either a list of headers or a list containing header=value pairs.
    headers = header if isinstance(header, list) else [header]
    parsed = []
    for h in headers:
        if '=' in h:
            k, v = h.split('=', 1)
            parsed.append((k, v))
        else:
            parsed.append(h)
    # ... use `parsed` with clear semantics
```

Add/adjust unit tests to lock in the contract (signature compatibility, parsing shapes, and runtime return types).