---
title: Use specific descriptive names
description: Choose names that clearly indicate the specific purpose, scope, or domain
  of functions, variables, and types rather than using generic terms. Generic names
  like `is_start`, `is_middle`, `enable_ignore` can be ambiguous and require readers
  to examine implementation details to understand their meaning.
repository: opengrep/opengrep
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 1546
---

Choose names that clearly indicate the specific purpose, scope, or domain of functions, variables, and types rather than using generic terms. Generic names like `is_start`, `is_middle`, `enable_ignore` can be ambiguous and require readers to examine implementation details to understand their meaning.

Prefer specific, descriptive names that immediately convey what the identifier does or represents:

```ocaml
(* Instead of generic names *)
let is_start (l : single_line) : bool = ...
let is_middle (l : single_line) : bool = ...
let enable_ignore = false

(* Use specific, descriptive names *)
let is_if_start (l : single_line) : bool = ...
let is_else_start (l : single_line) : bool = ...
let apply_ignore_pattern = false
```

This principle also applies to type names - ensure they clearly communicate their purpose and distinguish them from similar types in the codebase. When names might still be unclear despite being specific, add clear documentation explaining the rationale behind the naming choice.