---
title: prefer built-in error utilities
description: Use existing error handling utilities and appropriate error mechanisms
  instead of implementing manual error handling logic. This reduces code complexity,
  improves maintainability, and leverages well-tested library functions.
repository: opengrep/opengrep
label: Error Handling
language: Other
comments_count: 4
repository_stars: 1546
---

Use existing error handling utilities and appropriate error mechanisms instead of implementing manual error handling logic. This reduces code complexity, improves maintainability, and leverages well-tested library functions.

For regex operations, prefer functions like `pmatch_noerr` that handle errors automatically:
```ocaml
(* Instead of manual error handling *)
match Pcre2_.pmatch ~rex:url_regex config_path with
| Ok true -> true
| Ok false -> false 
| Error err ->
    Log.warn (fun m -> m "Error Validation URL: %a" pp_error err);
    false

(* Use built-in error handling *)
let is_url config_path = Pcre2_.pmatch_noerr ~rex:url_regex config_path
```

For impossible cases, choose appropriate mechanisms: use `assert false` for truly impossible conditions, provide clear error messages for invalid input ("at least one target required" rather than "bug: no valid target"), or refactor to eliminate impossible cases entirely.

For conditional error handling, structure logic clearly with explicit branching rather than complex nested error propagation.