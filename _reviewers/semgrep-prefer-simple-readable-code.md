---
title: prefer simple readable code
description: Choose clarity and simplicity over clever or complex constructs. Avoid
  unnecessary abstractions, complex function compositions, and "clever" code patterns
  that sacrifice readability for brevity.
repository: semgrep/semgrep
label: Code Style
language: Other
comments_count: 9
repository_stars: 12598
---

Choose clarity and simplicity over clever or complex constructs. Avoid unnecessary abstractions, complex function compositions, and "clever" code patterns that sacrifice readability for brevity.

**Key principles:**
- Use direct, explicit code over complex function compositions like `Option.map (Fun.const true)`
- Prefer simple conditionals over polymorphic variants with unnecessary indirection
- Choose appropriate built-in functions (`List.exists` for boolean checks, `String.starts_with` over manual substring comparison)
- Avoid polymorphic equality operators when specific ones are available
- Extract helper functions to eliminate code duplication rather than repeating complex logic

**Example:**
```ocaml
(* Avoid: clever but hard to read *)
code_config = Option.map (Fun.const true) code_config

(* Prefer: explicit and clear *)
match code_config with 
| None -> false 
| Some _ -> true

(* Or even simpler *)
Option.is_some code_config
```

The goal is code that any team member can quickly understand and modify. When choosing between a clever one-liner and a few clear lines, prefer clarity. This improves maintainability and reduces the cognitive load for future developers working with the code.