---
title: Benchmark performance assumptions
description: Always validate performance concerns with actual measurements before
  making optimization decisions. Avoid making assumptions about what is "too slow"
  without benchmarking evidence.
repository: semgrep/semgrep
label: Performance Optimization
language: Other
comments_count: 4
repository_stars: 12598
---

Always validate performance concerns with actual measurements before making optimization decisions. Avoid making assumptions about what is "too slow" without benchmarking evidence.

When performance issues are confirmed through benchmarks, optimize strategically by:
- Minimizing expensive operations (e.g., avoid repeated calls to costly functions like `Fpath.v`)
- Eliminating unnecessary allocations (e.g., avoid constructing intermediate lists when direct iteration is possible)
- Caching expensive computations at parse-time rather than recomputing them repeatedly

Example of evidence-based decision making:
```ocaml
(* Initial assumption: "We cannot afford to call Unix.realpath for each path because it's too slow" *)
(* After benchmarking: "running Semgrep with all free and Pro rules on 38 repos, and seeing no difference in perf wrt baseline" *)
(* Conclusion: "clearly we can afford Unix.realpath" *)
```

Example of strategic optimization:
```ocaml
(* Inefficient: constructing unnecessary intermediate lists *)
let trace_tokens = trace |> List.concat_map tokens_of_trace_item in
let filenames = trace_tokens |> List.map get_filename in

(* Better: direct iteration without intermediate allocations *)
let filenames = trace |> List.fold_left (fun acc item -> 
  get_filename_from_item item :: acc) [] |> List.rev in
```

This approach prevents both premature optimization and performance regressions by ensuring decisions are grounded in measurable data.