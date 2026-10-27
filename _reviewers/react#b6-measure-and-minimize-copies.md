---
title: Measure and minimize copies
description: 'When a change can affect performance (data structure size/layout or
  control-flow/state propagation), do two things: (1) quantify and document the impact
  with profiling, and (2) remove avoidable copying by using ownership/move on the
  final use instead of cloning for every iteration.'
repository: facebook/react#b6
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251888
---

When a change can affect performance (data structure size/layout or control-flow/state propagation), do two things: (1) quantify and document the impact with profiling, and (2) remove avoidable copying by using ownership/move on the final use instead of cloning for every iteration.

- For layout/serialization changes (e.g., adding fields):
  - Check struct/type growth on the target architecture and measure runtime impact.
  - Profile to find the real hotspot; don’t assume the slowdown comes from obvious adjacent code paths.
  - If the change is necessary, consider more compact representations (e.g., sentinel values vs `Option`) and/or `serde` attributes to avoid serializing fields that don’t belong.

- For state propagation across successors/branches:
  - If you only need the value for multiple successors but can consume it on the last one, structure the loop so earlier successors clone and the last one moves.
  - Keep readability: iterator-based approaches are fine as long as they preserve the “move on last use” optimization.

Example (move on last successor):
```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let last = successors.len();
let mut state = Some(state);
for (i, next_block_id) in successors.into_iter().enumerate() {
    let outgoing = if i + 1 == last {
        state.take().expect("state is taken only on the last successor")
    } else {
        state.as_ref().expect("state is live until the last successor").clone()
    };

    // process outgoing state for next_block_id
}
```

Rule of thumb: if you’re going to accept a measurable regression from added cost, back it with profiling; if you’re copying data in loops, see whether the last iteration can move instead of clone.