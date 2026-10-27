---
title: Measure and avoid overhead
description: 'For performance-sensitive code, treat both *data layout changes* and
  *unnecessary cloning* as first-class costs: (1) measure impact and profile to identify
  the real bottleneck, and (2) structure code to avoid avoidable overhead (larger
  structs, extra clones) while keeping the same semantics.'
repository: facebook/react#b4
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251885
---

For performance-sensitive code, treat both *data layout changes* and *unnecessary cloning* as first-class costs: (1) measure impact and profile to identify the real bottleneck, and (2) structure code to avoid avoidable overhead (larger structs, extra clones) while keeping the same semantics.

Apply:
- When changing core/HIR/IR types or serialized structures: run before/after benchmarks and confirm where time is spent (e.g., lowering/IR passes vs parsing). If a field increases struct size, consider cheaper representations (e.g., sentinel values instead of `Option` when it reduces size) and document the tradeoff.
- In dataflow/CFG successor propagation: ensure the last successor *moves* state while earlier successors get clones only as needed. Prefer loop/iterator patterns that preserve the “clone until last, then move” optimization.

Example (move on last successor):
```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let last = successors.len();
let mut state = Some(state);

for (i, next_block_id) in successors.into_iter().enumerate() {
    // Clone only if this is not the last successor; otherwise move.
    let outgoing = if i + 1 == last {
        state.take().expect("state taken only on last successor")
    } else {
        state.as_ref().expect("state still live").clone()
    };

    // ... use outgoing for next_block_id
}
```

This keeps performance work grounded in evidence and focuses developer effort on the highest-leverage overheads (memory/layout and cloning/moves).