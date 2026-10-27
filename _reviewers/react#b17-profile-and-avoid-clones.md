---
title: Profile and avoid clones
description: When working in performance-sensitive code, (1) quantify and document
  real costs for any extra memory/layout/serialization overhead, and (2) write control
  flow to avoid unnecessary cloning/copies in hot loops.
repository: facebook/react#b17
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251891
---

When working in performance-sensitive code, (1) quantify and document real costs for any extra memory/layout/serialization overhead, and (2) write control flow to avoid unnecessary cloning/copies in hot loops.

1) Quantify & document overhead
- If a struct change increases size or serialization payload, run release benchmarks and/or profiling to find where time moves.
- Include the measured impact (e.g., “+2.1% median; lowering +5%, EnterSSA +8.5%”) in the PR description (or an internal comment) and explicitly state why the tradeoff is acceptable.

2) Avoid cloning when you can move
- For loops that “branch” on multiple successors/targets, structure ownership so the last consumer takes ownership while earlier consumers clone only when needed.

Example pattern (move on last successor):

```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let last = successors.len();
let mut state = Some(state);
for (i, next_block_id) in successors.into_iter().enumerate() {
    let outgoing = if i + 1 == last {
        state.take().expect("taken on last successor")
    } else {
        state.as_ref().expect("state live until last").clone()
    };

    // use outgoing for next_block_id
}
```

Equivalent iterator-based approaches are also encouraged as long as they preserve the same optimization (clone for N-1, move for the last).