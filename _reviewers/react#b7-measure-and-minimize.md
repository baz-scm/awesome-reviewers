---
title: Measure and minimize
description: 'When making performance-affecting changes, do two things:


  1) **Quantify and document the tradeoff**

  - If a change alters struct layout, serialization size, or hot-path behavior, measure
  the impact in release builds and record: observed time/memory delta and what profiling
  attributed the cost to.'
repository: facebook/react#b7
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251888
---

When making performance-affecting changes, do two things:

1) **Quantify and document the tradeoff**
- If a change alters struct layout, serialization size, or hot-path behavior, measure the impact in release builds and record: observed time/memory delta and what profiling attributed the cost to.
- If you keep a “straightforward” implementation despite overhead, document the numbers so future reviews can make informed decisions.

2) **Minimize cloning and allocations in hot logic**
- For fan-out/fan-in successor handling, ensure the “last” successor can **take ownership** while earlier successors receive **clones** only as needed.
- Prefer Rust iterator patterns that preserve this optimization and reduce error-prone Option/expect branching.

Example pattern (n-1 clones + 1 move):
```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let outgoing_states = std::iter::repeat_n(state, successors.len());
for (next_block_id, outgoing) in successors.into_iter().zip(outgoing_states) {
    // Use `outgoing` knowing the original is moved exactly once
    // and prior iterations only cloned as required.
    process_successor(next_block_id, outgoing);
}
```

Apply this standard in reviews for any change touching memory layout/serialization, or code paths executed repeatedly in compilation/analysis loops.