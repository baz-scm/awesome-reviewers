---
title: avoid failwith patterns
description: 'Avoid using `failwith`, `assert false`, and similar blunt error handling
  mechanisms that can turn recoverable errors into unrecoverable ones. Instead, prefer
  more robust approaches:'
repository: semgrep/semgrep
label: Error Handling
language: Other
comments_count: 9
repository_stars: 12598
---

Avoid using `failwith`, `assert false`, and similar blunt error handling mechanisms that can turn recoverable errors into unrecoverable ones. Instead, prefer more robust approaches:

**Use pattern matching over exception handling:**
```ocaml
(* Avoid *)
let params = if is_method then
    let (lb, ps', rb) = def.G.fparams in
    (lb, (try List.tl ps' with Failure _ -> ps'), rb)

(* Prefer *)
let params = if is_method then
    let (lb, ps', rb) = def.G.fparams in
    match ps' with
    | [] -> (lb, ps', rb)
    | _ :: tl -> (lb, tl, rb)
```

**Use Result types for error-prone operations:**
```ocaml
(* Avoid Either.t, prefer Result.t *)
val load_rules_from_file : ... -> (rules_and_origin, Rule.error) Result.t
```

**Choose appropriate exception types:**
- Use `Invalid_argument` for caller bugs (indicates misuse of API)
- Use `failwith` with descriptive messages only when errors are genuinely expected
- Avoid `assert false` unless you're absolutely certain the case is impossible

**Handle dangerous operations safely:**
```ocaml
(* Avoid *)
let repository_path = url |> Git_wrapper.temporary_remote_checkout_path |> Option.get

(* Prefer *)
match Git_wrapper.temporary_remote_checkout_path url with
| Some path -> path
| None -> Error.abort "Failed to create temporary checkout path"
```

This approach prevents crashes from supposedly "impossible" cases (especially after error recovery), allows for better error propagation, and makes code more maintainable by explicitly handling edge cases.