---
title: Profile and minimize
description: When making performance-sensitive changes, (1) quantify the impact with
  benchmarks/profiling and (2) implement code that minimizes unnecessary allocations/clones
  in hot paths.
repository: facebook/react#b10
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251894
---

When making performance-sensitive changes, (1) quantify the impact with benchmarks/profiling and (2) implement code that minimizes unnecessary allocations/clones in hot paths.

How to apply
- For any change that affects data layout, serialization payloads, or core compiler pipeline steps, run representative benchmarks and use a profiler to identify where the time/memory cost lands. Don’t rely on assumptions like “it’s just two fields.”
- For hot-path logic that propagates state to multiple successors/items, clone only when required; prefer moving/`take()` for the last consumer to avoid an extra copy.

Example (minimize cloning for successors)
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

    // process next_block_id with `outgoing`
}
```

Also acceptable: a cleaner pattern that preserves “clone n-1, move 1” semantics.
```rust
let outgoing_states = std::iter::repeat_n(state, successors.len());
for (next_block_id, outgoing) in successors.into_iter().zip(outgoing_states) {
    // process next_block_id with `outgoing`
}
```

Standard outcome: every performance-impacting PR should (a) show the measured cost and likely bottleneck(s), and (b) avoid avoidable cloning/copying in tight loops/state propagation.