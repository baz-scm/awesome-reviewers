---
title: Measure and Avoid Overhead
description: When touching performance-sensitive code, (1) quantify the impact of
  structural changes and (2) avoid avoidable runtime overhead (especially cloning/allocation)
  by using ownership-aware control flow.
repository: facebook/react#b14
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251893
---

When touching performance-sensitive code, (1) quantify the impact of structural changes and (2) avoid avoidable runtime overhead (especially cloning/allocation) by using ownership-aware control flow.

Apply this as a lightweight standard:
- For data-structure/layout changes: run release benchmarks (or targeted microbenchmarks), compare median/percent deltas, and profile to confirm where the cost comes from. If you keep a change despite overhead, document the numbers and bottleneck attribution in the PR/commit description.
- For hot-path propagation/looping: avoid cloning values unless multiple consumers truly require it. Prefer patterns that move the value to the last consumer and clone only for earlier ones.

Example (ownership for last iteration, preserving “clone N-1 times”):
```rust
let last = successors.len();
let mut state = Some(state);
for (i, next_block_id) in successors.into_iter().enumerate() {
    let outgoing = if i + 1 == last {
        state.take().expect("taken only on last successor")
    } else {
        state
            .as_ref()
            .expect("state live until last successor")
            .clone()
    };

    // use next_block_id + outgoing
}

// Or, if it fits your API/ownership model:
// let outgoing_states = std::iter::repeat_n(state, successors.len());
// ...
```

This keeps performance changes intentional: you’ll either eliminate overhead (through ownership/iteration) or justify it with measured, profiled evidence.