---
title: Semantic Identifier Rules
description: 'Ensure identifiers and boolean helpers are semantically precise and
  safe.


  - Boolean predicates: if the function answers “does any item satisfy X?”, name it
  `hasX` (or `containsX`) rather than `isX`. For example, for a list of details:'
repository: facebook/react#b1
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 251878
---

Ensure identifiers and boolean helpers are semantically precise and safe.

- Boolean predicates: if the function answers “does any item satisfy X?”, name it `hasX` (or `containsX`) rather than `isX`. For example, for a list of details:
  - Prefer: `hasError(): boolean` (true if any detail has `ErrorSeverity.Error`)
  - Avoid: `isError()` when it isn’t equivalent to “all details are Error”.

- Generated names in transformations/codegen: when turning user-facing names into internal identifiers (e.g., sanitizing `aria-label`), don’t rely on an incomplete local dedupe set for uniqueness. Use the compiler’s scoped UUID/identifier generator (e.g., `programContext.newUuid()` / equivalent) so collisions can’t occur across the compilation pipeline.

- Special syntactic cases: if an input has a distinct representation (e.g., numeric object property keys), model it explicitly (e.g., a dedicated `ObjectPropertyKey` variant) instead of relying on implicit conversion rules that blur meaning.

Applying this consistently makes naming clearer, reduces snapshot churn/collisions, and prevents future logic bugs from ambiguous semantics.