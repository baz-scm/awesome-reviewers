---
title: Measure And Avoid Clones
description: 'For performance-sensitive code, pair evidence with efficient state propagation:


  1) Measure and attribute before/after

  - If a change affects memory layout, serialization cost, or hot-path structures,
  benchmark (release) and record the impact.'
repository: facebook/react#b5
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251886
---

For performance-sensitive code, pair evidence with efficient state propagation:

1) Measure and attribute before/after
- If a change affects memory layout, serialization cost, or hot-path structures, benchmark (release) and record the impact.
- Use profiling to identify what actually regressed (e.g., lowering/SSA passes) so the team can reason about root cause.
- If you accept a tradeoff, document the measured cost and where it shows up.

2) Avoid unnecessary cloning in hot loops
- When the same analysis/state must be sent to multiple successors, keep cloning to the minimum by moving into the last consumer and cloning only for earlier ones.

Example pattern (move into last, clone otherwise):
```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let last = successors.len();
let mut state = Some(state);

for (i, next_block_id) in successors.into_iter().enumerate() {
    let outgoing = if i + 1 == last {
        state.take().expect("taken only on last successor")
    } else {
        state.as_ref().expect("state stays live until last")
             .clone()
    };

    // use outgoing for next_block_id
}
```
Or simplify while preserving the “move once” optimization:
```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let outgoing_states = std::iter::repeat_n(state, successors.len());
for (next_block_id, outgoing) in successors.into_iter().zip(outgoing_states) {
    // use outgoing for next_block_id
}
```

Apply this standard to any change that could affect CPU time or memory pressure, and keep the implementation both fast and explainable via measured tradeoff notes.