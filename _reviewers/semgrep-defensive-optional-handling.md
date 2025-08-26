---
title: Defensive optional handling
description: Always handle optional and nullable values defensively by checking for
  null/empty states before use and handling multiple optional values independently.
  Use explicit null coalescing patterns to provide safe defaults, and avoid nesting
  optional value logic when they should be processed independently.
repository: semgrep/semgrep
label: Null Handling
language: Other
comments_count: 3
repository_stars: 12598
---

Always handle optional and nullable values defensively by checking for null/empty states before use and handling multiple optional values independently. Use explicit null coalescing patterns to provide safe defaults, and avoid nesting optional value logic when they should be processed independently.

Key practices:
1. Check for empty/null values before operations that could fail
2. Handle multiple optional parameters independently rather than nesting their logic
3. Use null coalescing operators or patterns for safe defaults

Example from the codebase:
```ocaml
(* Good: Independent handling of multiple optionals *)
match opt1 with
| None -> []
| Some (_, st1) -> [st1]
@
match opt2 with  (* Handle opt2 independently *)
| None -> []
| Some (_, st2) -> [st2]

(* Good: Defensive check before use *)
let loc =
  if not String.(equal file "") then Tok.first_loc_of_file file
  else default_loc

(* Good: Null coalescing pattern *)
let result = optional_value ||| default_value
```

This prevents runtime errors from unexpected null/undefined values and ensures all optional cases are properly handled.