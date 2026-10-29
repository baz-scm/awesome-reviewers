---
title: Use Sphinx cross-reference roles
description: 'When documentation or NEWS entries mention a Python identifier, RFC,
  or glossary term, use the matching Sphinx role instead of plain text or double backticks,
  so the reference becomes a clickable, validated link. Pick the role that matches
  the actual kind of object: `:mod:` for modules, `:func:` for module-level functions,
  `:meth:` for methods,...'
repository: python/cpython
label: Documentation
language: Other
comments_count: 18
repository_stars: 77696
---

When documentation or NEWS entries mention a Python identifier, RFC, or glossary term, use the matching Sphinx role instead of plain text or double backticks, so the reference becomes a clickable, validated link. Pick the role that matches the actual kind of object: `:mod:` for modules, `:func:` for module-level functions, `:meth:` for methods, `:class:`/`:exc:` for classes and exceptions, `:const:`/`:attr:`/`:data:` for constants, attributes and module data, `:rfc:` for RFCs, and `:term:`/`:ref:` for glossary terms or named sections. Only fall back to plain `` ``code`` `` markup for things that aren't documented objects (e.g. private/internal names, non-public attributes, or implementation-only functions), since roles that target undocumented objects will fail the doc build.

For example, instead of:

```rst
Fix memory leak in sqlite3.Connection.load_extension() when error is
returned
```

write:

```rst
Fix memory leak in :meth:`sqlite3.Connection.load_extension` when
:exc:`sqlite3.OperationalError` is raised.
```

Likewise, prefer `:rfc:`6265`` over ` ``RFC 6265`` `, and `:mod:`http.cookies`` over ` ``http.cookies`` `. Applying the correct role consistently keeps the rendered docs properly cross-linked and catches broken or misnamed references at build time.