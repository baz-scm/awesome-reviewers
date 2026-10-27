---
title: Profile and avoid clones
description: 'Treat performance-impacting changes as intentional engineering work:
  (1) measure and document runtime/memory effects, and (2) implement targeted reductions
  in allocation/cloning.'
repository: facebook/react#b16
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251891
---

Treat performance-impacting changes as intentional engineering work: (1) measure and document runtime/memory effects, and (2) implement targeted reductions in allocation/cloning.

**1) For data layout/serialization changes, benchmark + attribute the cost**
- If you add fields that change struct sizes or serialization payloads, run the relevant benchmarks and capture the delta.
- Attribute the slowdown (e.g., via profiling) and either (a) justify the tradeoff in the code review, (b) reduce the size (e.g., packing/sentinels), or (c) avoid the change if it’s not worth it.

**2) For branch/state propagation, minimize clones with ownership transfer**
- When a value is reused across multiple successors, clone only what’s needed; move (take) the owned value into the last successor and clone for earlier ones.
- Keep the code readable; iterator helpers are fine as long as they preserve the “clone only n-1 times, move once” behavior.

Example pattern (clone for all but last, move for last):
```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let last = successors.len();
let mut state = Some(state);

for (i, next_block_id) in successors.into_iter().enumerate() {
    let outgoing = if i + 1 == last {
        state.take().expect("taken only on the last successor")
    } else {
        state.as_ref().expect("state live until last").clone()
    };

    // ... use outgoing for next_block_id
}
```

If you refactor with iterators, ensure you still preserve the same clone/move counts (e.g., `repeat_n(...).zip(...)`), rather than introducing extra copies.