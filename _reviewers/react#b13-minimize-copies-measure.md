---
title: Minimize Copies, Measure
description: When performance or memory could be affected, (1) design dataflow/state
  propagation to avoid unnecessary cloning by moving ownership where possible, and
  (2) for changes that may increase object/struct sizes, back the decision with benchmarks/profiling
  and document the tradeoff.
repository: facebook/react#b13
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251893
---

When performance or memory could be affected, (1) design dataflow/state propagation to avoid unnecessary cloning by moving ownership where possible, and (2) for changes that may increase object/struct sizes, back the decision with benchmarks/profiling and document the tradeoff.

Apply this as a standard:
- For successor/branch propagation, ensure only the needed paths clone, and allow the last successor to take ownership.
- Where you can, use iterator-based patterns to keep the implementation clean while preserving the “clone only when required; move on last” optimization.
- If a change increases struct size/layout, measure the impact (benchmarks + profiler) and record what actually regressed/improved.

Example (avoid cloning on the last successor):
```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let last = successors.len();
let mut state = Some(state);
for (i, next_block_id) in successors.into_iter().enumerate() {
    let outgoing = if i + 1 == last {
        state.take().expect("taken only on last")
    } else {
        state.as_ref().expect("state live until last").clone()
    };
    // use outgoing for next_block_id
}
```
If you change representations (e.g., adding fields that alter layout/size), confirm the effect with real measurements and profiling (identify the true bottleneck) before deciding to keep the simpler implementation.