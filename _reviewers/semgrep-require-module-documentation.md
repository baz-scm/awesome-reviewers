---
title: require module documentation
description: 'All modules containing functions should have corresponding .mli files
  with comprehensive documentation. The .mli file must include:


  1. **Module purpose**: A clear, high-level description of what the module does and
  why it exists'
repository: semgrep/semgrep
label: Documentation
language: Other
comments_count: 11
repository_stars: 12598
---

All modules containing functions should have corresponding .mli files with comprehensive documentation. The .mli file must include:

1. **Module purpose**: A clear, high-level description of what the module does and why it exists
2. **Function documentation**: Comments explaining what each function does, its parameters, return values, and any special behaviors
3. **Type documentation**: Clear explanations of custom types and their fields
4. **API behavior notes**: Documentation of important behaviors like error handling, redirects, or resource management

Example structure:
```ocaml
(** High-level module purpose and goals.
    
    This module handles X by doing Y, and is primarily used for Z.
    See also {!Related_module} for similar functionality.
*)

(** Custom type representing... *)
type analysis_flags = {
  secrets_validators : bool; (** Enable secrets validation *)
  historical_scan : bool;    (** Scan historical data *)
  (* ... *)
}

(** Execute a command request.
    
    @param request The command to execute
    @param context Current execution context
    @return Result of execution or error
    
    Note: Automatically handles 307 redirects for binary downloads.
*)
val handle_execute_request : request -> context -> (result, error) Result.t
```

This ensures that module interfaces are self-documenting and that ocamldoc can generate useful documentation. Avoid vague function names without proper documentation, and always explain the module's role in the larger system.