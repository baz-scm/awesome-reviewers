---
title: Choose efficient algorithms
description: When implementing algorithms, prioritize computational efficiency by
  selecting appropriate data structures and avoiding unnecessarily complex approaches.
  Consider the time complexity of your solution and whether built-in functions or
  better data structures could improve performance.
repository: semgrep/semgrep
label: Algorithms
language: Other
comments_count: 5
repository_stars: 12598
---

When implementing algorithms, prioritize computational efficiency by selecting appropriate data structures and avoiding unnecessarily complex approaches. Consider the time complexity of your solution and whether built-in functions or better data structures could improve performance.

Key principles:
- Use built-in functions that provide early exit behavior instead of manual exception handling
- Choose appropriate data structures (sets for deduplication, hash tables for lookups)
- Avoid expensive operations like JSON serialization for equality comparisons
- Be mindful of quadratic complexity, especially when processing large datasets

Examples of improvements:

Instead of manual exception handling for early exit:
```ocaml
(* Avoid *)
try
  List.fold_left (fun _ x -> 
    if condition x then raise (Found x)) () lst
with Found x -> Some x

(* Prefer *)
List.find_opt condition lst
```

Instead of manual folding for set operations:
```ocaml
(* Avoid *)
List.fold_left (fun acc m -> StringSet.add m.path acc) StringSet.empty matches

(* Prefer *)
matches |> List.map (fun m -> m.path) |> Set_.of_list
```

Instead of expensive equality comparisons:
```ocaml
(* Avoid *)
let a_json = a |> to_json |> to_string in
let b_json = b |> to_json |> to_string in
String.equal a_json b_json

(* Prefer *)
Common2.on String.equal extract_key a b
```

When dealing with potentially large datasets, document the time complexity and consider whether O(N²) algorithms need optimization. For stack-intensive operations, prefer iterative approaches or tail-recursive functions to avoid stack overflow issues.