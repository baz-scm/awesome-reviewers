---
title: Document Behavior Changes
description: 'Update documentation every time code behavior changes or new public
  APIs are introduced.


  Apply this checklist:

  1) Docstring accuracy: If you change semantics (error handling, return values, shutdown
  behavior, etc.), update the docstring to match reality.'
repository: celery/celery
label: Documentation
language: Python
comments_count: 8
repository_stars: 28464
---

Update documentation every time code behavior changes or new public APIs are introduced.

Apply this checklist:
1) Docstring accuracy: If you change semantics (error handling, return values, shutdown behavior, etc.), update the docstring to match reality.
2) Public API versioning: For any new/changed public method, add the appropriate Sphinx directive (`.. versionadded:: X.Y.Z` / `.. versionchanged:: X.Y.Z`) consistently (including any related backend/base/async docstrings).
3) User-facing docs: If behavior impacts users (e.g., shutdown semantics, retries, connection handling), update the relevant documentation section and include a version note.
4) Interface/contract documentation: For new classes/steps that implement an interface, add inline documentation describing the contract/expected behavior.
5) Docs tooling for optional deps: Prefer Sphinx mechanisms like `autodoc_mock_imports` for optional third-party dependencies so API docs build without hiding misconfiguration.

Example (public API versioning + docstring alignment):
```python
class BaseBackend:
    def exists(self, task_id: str) -> bool:
        """Return True if a result exists for the given task id."""
        # ...

        .. versionadded:: 5.7.0
```

Example (doc update for shutdown semantics):
- If code changes shutdown to cancel pending work, ensure the worker docs’ “Warm Shutdown” section describes the new behavior and includes `.. versionchanged:: X.Y`.