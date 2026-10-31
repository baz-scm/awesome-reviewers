---
title: Accurate, consistent documentation
description: 'Documentation and comments must be accurate, concise, and follow the
  project''s established conventions so they stay trustworthy and maintainable.


  - Describe actual behavior precisely. Avoid misleading wording (e.g., don''t say
  "a copy of the session" is used when it''s actually the same object reference—say
  "the current session object is used instead of...'
repository: pallets/flask
label: Documentation
language: Python
comments_count: 5
repository_stars: 75022
---

Documentation and comments must be accurate, concise, and follow the project's established conventions so they stay trustworthy and maintainable.

- Describe actual behavior precisely. Avoid misleading wording (e.g., don't say "a copy of the session" is used when it's actually the same object reference—say "the current session object is used instead of reloading the original data").
- Keep comments focused on *why* the code does something, not on explaining language semantics. For example, replace a verbose explanation of Python 3's exception scoping with a short note like `# make error available outside except block (py3)`.
- Record behavior changes using the proper Sphinx directives (`.. versionadded::`, `.. versionchanged::`) instead of rewriting prose that loses the version history.
- Don't duplicate data that can drift out of sync (e.g., default environment values). Instead, reference the single source of truth, such as pointing to `client.environ_base` rather than hardcoding the same dict in the docstring.
- Follow existing codebase conventions for inline documentation. In Flask, class-level attributes are documented using the `#:` comment style rather than a "dangling" docstring placed after the assignment:

```python
class JSONTag(object):
    #: The tag to mark the serialized object with. If ``None``, this tag is
    #: considered mapping key.
    key = None
```

Applying these practices prevents stale or misleading docs, keeps comments meaningful, and ensures documentation renders correctly and consistently across the codebase.</description>
</invoke>
