---
title: Context-aware algorithm selection
description: Choose algorithms and data structures based on operational requirements
  and usage context rather than defaulting to familiar patterns. Consider factors
  like compilation timing, API constraints, and different execution contexts when
  making design decisions.
repository: opengrep/opengrep
label: Algorithms
language: Other
comments_count: 5
repository_stars: 1546
---

Choose algorithms and data structures based on operational requirements and usage context rather than defaulting to familiar patterns. Consider factors like compilation timing, API constraints, and different execution contexts when making design decisions.

Key principles:
1. **Analyze operational requirements**: Store data in forms that support required operations. For example, if you need compilation flags later, store the full compiled object rather than just the raw string.

2. **Eliminate algorithmic redundancy**: Consolidate redundant pattern matching cases and prefer functional approaches over imperative ones when appropriate.

3. **Respect API constraints**: Understand the limitations of your tools and APIs. For instance, if `Fpath.add_seg` only accepts filenames, design your interface accordingly.

4. **Context-dependent processing**: Use different algorithms for different contexts. The same syntax may require different parsing strategies in patterns versus programs.

Example of context-aware data structure choice:
```ocaml
(* Instead of storing just the pattern string *)
| MvarRegexp (mvar, re_str, const_prop) ->
    let re = Pcre2_.pcre_compile re_str in
    (* Store the compiled object to avoid recompilation *)

(* Consider compilation context and flags *)
let re = match Pcre2_.remove_end_of_string_assertions compiled_re with
  | None -> raise GeneralPattern  
  | Some re -> re
```

This approach leads to more efficient, maintainable code that adapts appropriately to different operational contexts and constraints.