---
title: Measure and Minimize Work
description: For performance-sensitive code, (1) quantify any data-structure or serialization
  change with benchmark deltas and profiling, and (2) minimize runtime work by avoiding
  unnecessary clones via ownership-aware iteration.
repository: facebook/react#b12
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251896
---

For performance-sensitive code, (1) quantify any data-structure or serialization change with benchmark deltas and profiling, and (2) minimize runtime work by avoiding unnecessary clones via ownership-aware iteration.

Apply it like this:
- When changing hot structs (especially ones carried through lowering/SSA or across serialization boundaries), estimate/measure size impact and include benchmark/profiling results in the change description (e.g., “+X% median; bottleneck in Y”). If the cost is real, explicitly justify the tradeoff.
- When propagating shared state to multiple successors/targets, clone only when you must. Prefer moving ownership into the last successor to avoid an extra clone; for straight-line blocks (single successor), the state should be moved with zero cloning.

Example pattern (move on last successor, clone earlier ones):

```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let last = successors.len();
let mut state = Some(state);

for (i, next_block_id) in successors.into_iter().enumerate() {
    let outgoing = if i + 1 == last {
        // Move on the final successor.
        state.take().expect("state is taken only on the last successor")
    } else {
        // Clone only for earlier successors.
        state.as_ref().expect("state is live until the last successor").clone()
    };

    // use outgoing...
}
```

Optionally, when it preserves the optimization, use iterator utilities to express the same behavior more cleanly.

This standard keeps performance work intentional and verifiable while preventing avoidable allocation/cloning overhead.