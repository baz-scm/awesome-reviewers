---
title: Measure and minimize copies
description: For performance-sensitive code, (1) quantify the impact of structural
  changes and (2) avoid unnecessary cloning/allocation in hot control-flow propagation.
repository: facebook/react#b11
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251894
---

For performance-sensitive code, (1) quantify the impact of structural changes and (2) avoid unnecessary cloning/allocation in hot control-flow propagation.

1) Quantify layout/serialization changes
- If adding fields (especially to types used in compilation pipelines or serialized formats) can change struct size or memory behavior, measure the effect (e.g., median slowdown %) and use profiling to identify the dominant hotspots before accepting the tradeoff.
- If possible, consider representation tweaks that reduce size (e.g., collapsing multiple option-like fields into a sentinel-based layout) and ensure comments/docstrings precisely describe semantics (e.g., how offsets differ from indices).

2) Minimize clones in successor/state propagation
- When propagating a state across multiple successors (CFG/IR traversal), only clone when you truly need parallel copies.
- For the last successor, transfer ownership so you don’t clone the final state.

Example pattern (move on last successor, clone otherwise):

```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let last = successors.len();
let mut state = Some(state);

for (i, next_block_id) in successors.into_iter().enumerate() {
    let outgoing = if i + 1 == last {
        state.take().expect("state is taken only on the last successor")
    } else {
        state
            .as_ref()
            .expect("state is live until the last successor")
            .clone()
    };

    // use outgoing for next_block_id
}
```

(Optionally, if it preserves the same move/clone behavior, consider iterator-based helpers to reduce branching, such as `std::iter::repeat_n`.)