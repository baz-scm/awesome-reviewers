---
title: Explicit API contracts
description: When an API accepts objects via duck typing (e.g., checking hasattr for
  a method) or restricts input to specific types, make the contract explicit rather
  than implicit. If a function intentionally narrows behavior to an exact type or
  restricts duck-typed objects (e.g., `PyDict_CheckExact()` excluding dict subclasses,
  or a fast path assuming `BytesIO`-like...
repository: python/cpython
label: API
language: Python
comments_count: 3
repository_stars: 77696
---

When an API accepts objects via duck typing (e.g., checking hasattr for a method) or restricts input to specific types, make the contract explicit rather than implicit. If a function intentionally narrows behavior to an exact type or restricts duck-typed objects (e.g., `PyDict_CheckExact()` excluding dict subclasses, or a fast path assuming `BytesIO`-like semantics for `getbuffer()`), add a comment or documentation explaining why, so future maintainers and reviewers understand the restriction is deliberate. Avoid introducing new implicit requirements (such as assuming `tell()` exists and returns a specific offset) on top of a loosely-defined duck-typed protocol, since objects that satisfy the documented interface but not the new unstated requirement will silently break — this is effectively a backward-incompatible API change even if it looks like a bugfix. When the exact-type behavior matters (performance fast path, special-cased semantics), prefer an explicit `isinstance()` check and fall back to the generic/duck-typed path for anything else, rather than relying on `hasattr` checks that assume a specific implementation's semantics. Similarly, when changing a long-standing default behavior could affect existing callers, prefer adding an explicit, documented opt-in parameter (e.g., `replace_duplicates=True`) instead of silently altering the default, so existing and new behaviors are both well-defined and backward compatible.