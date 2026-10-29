---
title: Accurate, synced documentation
description: 'Docstrings, comments, and reference docs must always reflect the current,
  actual behavior of the code, and all related documentation locations must be updated
  together. Concretely:'
repository: python/cpython
label: Documentation
language: Python
comments_count: 5
repository_stars: 77696
---

Docstrings, comments, and reference docs must always reflect the current, actual behavior of the code, and all related documentation locations must be updated together. Concretely:

- When changing a function/class's behavior, update or remove any outdated docstring text rather than leaving conflicting descriptions (e.g. don't keep a stale "dictionary style assignment" docstring next to new overwrite-prevention logic).
- Ensure the documented contract of a public API matches what the implementation actually supports. If docs say a method must return a subclass of `AbstractX`, the implementation should enforce/validate that, or the docs should be corrected to describe the real constraints and edge cases (e.g. virtual `register()`ed subclasses not working as documented).
- When a deprecation/removal timeline or version number changes, grep for and update every place it's mentioned (module source, `*.rst` reference pages, "What's New" entries, deprecation-timeline tables), not just the primary call site.
- Reserve full docstrings for public/user-facing APIs; for internal/private helper functions use a plain `#` comment instead of a triple-quoted docstring, since internal docstrings add no discoverability benefit and needlessly occupy memory.
- Follow standard docstring formatting: the first line should be a complete, standalone sentence under ~72 characters (many tools rely on this), and if you touch a multi-line docstring, bring all its lines into compliance (length, wrapping) rather than leaving a mix of fixed and unfixed lines.

Example of fixing a stale/misleading docstring:
```python
# Bad: docstring doesn't match the new behavior
def __setitem__(self, key, value):
    """Check if the key already exists, return without overwriting"""
    ...

# Good: update the docstring (or underlying logic) so both agree
def __setitem__(self, key, value):
    """Dictionary style assignment."""
    self.__set(key, value, ...)
```

Applying this consistently keeps documentation trustworthy, avoids contradicting the implementation, and prevents confusion when users or maintainers rely on docs/comments to understand behavior.</description>
