---
title: Clear unambiguous naming
description: Pick names (for functions, macros, and variables) that unambiguously
  convey their purpose and don't collide with existing identifiers that carry a different
  meaning in the same domain. Before naming, check whether a similar name already
  exists with different semantics elsewhere in the API/codebase (e.g. `PyFrozenSetWriter_Discard`
  is confusing next to...
repository: python/cpython
label: Naming Conventions
language: C
comments_count: 3
repository_stars: 77696
---

Pick names (for functions, macros, and variables) that unambiguously convey their purpose and don't collide with existing identifiers that carry a different meaning in the same domain. Before naming, check whether a similar name already exists with different semantics elsewhere in the API/codebase (e.g. `PyFrozenSetWriter_Discard` is confusing next to `set.discard()`, since one destroys a writer and the other removes an item); if a collision exists, choose a more specific name or follow an established naming family instead (e.g. reuse the Create/Finish/Discard convention already used by PyUnicodeWriter, PyBytesWriter, and PyLongWriter, and use suffixes like `DiscardItem` for item-level operations). Avoid vague or generic names such as `_constants_tuple_modified`; prefer names that state the action/outcome clearly, like `set_modified`, and keep macros/locals scoped close to their use. When a function's responsibility is generalized or its behavior changes (e.g. `inline_comprehension` renamed to `class_binds_free_name` so it can be reused in new contexts), make sure the new name still reflects what the function actually does without relying on unstated context, and update any accompanying comments so they match the new name/behavior rather than describing stale internal details (e.g. a "compressed delta") that only made sense under the old name.