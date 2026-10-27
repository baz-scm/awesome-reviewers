---
title: State-Flow Correctness
description: When propagating data through a transformation/CFG successor graph, preserve
  the invariants of the propagated identity/range data and encode state-flow intent
  explicitly.
repository: facebook/react#b15
label: Algorithms
language: Rust
comments_count: 3
repository_stars: 251891
---

When propagating data through a transformation/CFG successor graph, preserve the invariants of the propagated identity/range data and encode state-flow intent explicitly.

Apply this standard:
1) Preserve real indices/offsets (or make invalidity explicit)
- If a downstream consumer relies on `start_offset`/range correctness, ensure every path populates it from the real source (e.g., the real `loc.start.index` / node identity). If a path only has placeholders, either compute the correct offsets there or explicitly clear/avoid treating placeholders as real values.

2) Use explicit semantic variants instead of boolean flags
- If the meaning differs (e.g., Local vs Context), represent it as distinct variants (or distinct types), not as `... { is_context: bool }`. This prevents accidental mixing and makes future pattern matching safer.

3) In successor propagation, clone only when needed; move on the last edge
- Pattern: for a shared mutable state that must be given to multiple successor blocks, clone for all successors except the last, where you can transfer ownership.

Example (clone n-1 times, move on last):
```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let last = successors.len();
let mut state = Some(state);

for (i, next_block_id) in successors.into_iter().enumerate() {
    let outgoing = if i + 1 == last {
        state.take().expect("state is available only for the last successor")
    } else {
        state.as_ref().expect("state is live until the last successor").clone()
    };
    // use outgoing for next_block_id
}
```
Optionally, simplify with iterators (same behavior, clearer intent):
```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let outgoing_states = std::iter::repeat_n(state, successors.len());
for (next_block_id, outgoing) in successors.into_iter().zip(outgoing_states) {
    // use outgoing for next_block_id
}
```

Net effect: fewer correctness hazards (wrong offsets/blurred semantics) and less overhead (no unnecessary cloning), while keeping the state-flow logic easy to audit.