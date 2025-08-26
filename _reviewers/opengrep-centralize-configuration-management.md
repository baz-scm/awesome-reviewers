---
title: centralize configuration management
description: Configuration values should be defined in a single location and passed
  through proper data structures rather than duplicated across modules or stored in
  global state. This prevents inconsistencies, reduces error-prone code duplication,
  and improves maintainability.
repository: opengrep/opengrep
label: Configurations
language: Other
comments_count: 3
repository_stars: 1546
---

Configuration values should be defined in a single location and passed through proper data structures rather than duplicated across modules or stored in global state. This prevents inconsistencies, reduces error-prone code duplication, and improves maintainability.

Avoid defining default values in multiple places:
```ocaml
(* Bad: Duplicating default value *)
let semgrepignore_filename = Option.value conf.semgrepignore_filename ~default:".semgrepignore" in

(* Good: Use centralized default from Semgrepignore.ml *)
Semgrepignore.create ?semgrepignore_filename:conf.semgrepignore_filename
```

Replace global configuration state with proper data structures:
```ocaml
(* Bad: Global mutable state *)
let custom_ignore_pattern : string option ref = ref None

(* Good: Pass configuration through data types *)
type config = { custom_ignore_pattern: string option; ... }
let process_with_config config = ...
```

Ensure configuration consistency across different implementations (e.g., Python and OCaml components) by maintaining a single source of truth for feature flags and their requirements.