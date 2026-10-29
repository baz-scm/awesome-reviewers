---
title: Use idiomatic conventions
description: 'Write code that favors existing project idioms and clear control flow
  over ad hoc constructs, duplicated logic, or unnecessary complexity:


  - Avoid magic numbers; use the named constants the codebase already defines (e.g.
  `_Py_MAX_UNICODE` instead of hardcoding `0x10FFFF`), and use project-specific cast
  macros (e.g. `_PyMemoryView_CAST(v)`) instead of raw...'
repository: python/cpython
label: Code Style
language: C
comments_count: 9
repository_stars: 77696
---

Write code that favors existing project idioms and clear control flow over ad hoc constructs, duplicated logic, or unnecessary complexity:

- Avoid magic numbers; use the named constants the codebase already defines (e.g. `_Py_MAX_UNICODE` instead of hardcoding `0x10FFFF`), and use project-specific cast macros (e.g. `_PyMemoryView_CAST(v)`) instead of raw C-style casts.
- Keep casts minimal: don't chain casts (e.g. `(unsigned char)(unsigned long)x`) when a single cast suffices, and don't introduce casts/macros that only wrap a single trivial operation ("over-encapsulation")—inline the simple expression instead.
- Eliminate duplicated code blocks by factoring out the common expression or helper, e.g.:
  ```c
  // instead of duplicated if/else blocks setting a bool key:
  if (PyDict_SetItemString(dict, "immortal",
                            PyBool_FromLong(PyUnstable_IsImmortal(op))) < 0) {
      Py_DECREF(dict);
      return NULL;
  }
  ```
- Declare variables as close as possible to their point of use (e.g. move a declaration into the branch where it's actually assigned/used) to simplify reasoning about ownership/refcounting and remove unneeded cleanup code.
- Prefer assertions over comments to document invariants that can be checked at runtime (e.g. `assert(...)` instead of a comment claiming a value is always true).
- Avoid `goto` for anything other than the well-established "jump to cleanup/exit before returning" pattern; if logic requires a non-final jump, prefer extracting the logic into a separate function instead. When `goto` is used, give labels descriptive names (`format_errno`) rather than generic ones like `skip`.
- Multi-line macros must follow PEP 7's `do { ... } while (0)` wrapping to avoid dangling-else and similar pitfalls, and preprocessor conditionals should be simplified (e.g. collapse an `#if/#else` into a single `#if !defined(...)` when one branch becomes empty).

Applying these conventions keeps code consistent with the rest of the codebase, reduces redundancy, and makes control flow and ownership easier to follow during review and maintenance.</description>
</invoke>
