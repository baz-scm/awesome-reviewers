---
title: Accurate, consistent documentation
description: 'Keep all documentation (inline comments, docstrings, and changelog entries)
  accurate, concise, and consistent with established conventions. Specifically:'
repository: pallets/flask#x
label: Documentation
language: Python
comments_count: 6
repository_stars: 75163
---

Keep all documentation (inline comments, docstrings, and changelog entries) accurate, concise, and consistent with established conventions. Specifically:

- Comments should explain *why* code exists or clarify non-obvious intent, not restate language semantics or mechanics the reader is expected to know (e.g., prefer `# make error available outside except block (py3)` over a long explanation of Python 3's exception scoping).
- Docstrings must precisely describe behavior. Don't use misleading terms (e.g., say "the current session object is reused" rather than "a copy is added" if no copy actually occurs).
- Follow the project's established documentation style for consistency: use `#:` comments for documenting class/module-level attributes, and real docstrings (not trailing/dangling comments) for documenting methods, getters, and setters.
- Avoid duplicating details (such as default values or configuration) in multiple places like docstrings; instead, point to the single authoritative source (e.g., "see `client.environ_base` for defaults") so documentation doesn't drift out of sync with the code.
- Only add changelog/version-change notes for changes that affect public/user-facing behavior; skip changelog entries for internal-only or non-user-relevant changes.

Example of an accurate, properly placed docstring instead of a comment:
```python
@property
def debug(self):
    """Whether debug mode is enabled. When using ``flask run`` ..."""
    return self.config["DEBUG"]

@debug.setter
def debug(self, value):
    self.config["DEBUG"] = value
    self.jinja_env.auto_reload = self.templates_auto_reload
```
</description>
