---
title: Use descriptive names
description: Names should clearly and accurately describe their purpose, avoiding
  abbreviations, acronyms, and misleading terms. This applies to variables, functions,
  types, constructors, and modules.
repository: semgrep/semgrep
label: Naming Conventions
language: Other
comments_count: 9
repository_stars: 12598
---

Names should clearly and accurately describe their purpose, avoiding abbreviations, acronyms, and misleading terms. This applies to variables, functions, types, constructors, and modules.

**Key principles:**
- Prefer descriptive names over acronyms (use `dependency_mode` instead of `sca_mode`)
- Ensure type and constructor names accurately reflect their contents (use `RegularTarget` instead of `Code` for a data structure that doesn't contain code)
- Choose function names that reflect all parameters and functionality (avoid `code_of_origin` when passing multiple arguments beyond just an origin)
- Use clear variable names that are unambiguous in context (prefer `src` over `s` which could be confused with string)
- Avoid misleading terms that don't match actual functionality (don't use `CSV` for comma-separated parsing that doesn't handle CSV escaping)

**Example:**
```ocaml
(* Avoid *)
type sca_mode = [ `SCA of dependency_formula ]
let code_of_origin origin = ...
let parse_csv_from_env_vars vars = ...

(* Prefer *)
type dependency_mode = [ `Dependency of dependency_formula ]  
let mk_code_target xlang products origin = ...
let read_comma_separated_from_env_vars vars = ...
```

Names are the primary way developers understand code intent. Descriptive names reduce cognitive load, prevent misunderstandings, and make code self-documenting.