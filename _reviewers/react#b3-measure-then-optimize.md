---
title: Measure Then Optimize
description: 'For performance-sensitive code, first quantify impact, then implement
  the cheapest safe optimization.


  **How to apply**

  1. **Measure before accepting tradeoffs:** When you change core data structures
  (size/serde shape) or algorithms, use benchmarks and/or profiling to identify where
  time is spent (e.g., lowering/SSA vs. unrelated stages). Document the...'
repository: facebook/react#b3
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 251883
---

For performance-sensitive code, first quantify impact, then implement the cheapest safe optimization.

**How to apply**
1. **Measure before accepting tradeoffs:** When you change core data structures (size/serde shape) or algorithms, use benchmarks and/or profiling to identify where time is spent (e.g., lowering/SSA vs. unrelated stages). Document the measured delta and the profiled bottleneck.
2. **Eliminate avoidable overheads:**
   - Prefer designs that avoid extra struct bloat from optional fields when it meaningfully increases memory footprint.
   - In control-flow/state propagation, avoid cloning on every successor when only the last needs ownership—clone exactly `n-1` times and move once.
3. **Keep it idiomatic:** Use iterator utilities and clear ownership patterns so performance intent is obvious and hard to regress.

**Example (move on last, no Option/expect branches)**
```rust
let successors = terminal_successors(&func.body.blocks[&block_id].terminal);
let outgoing_states = std::iter::repeat_n(state, successors.len());
for (next_block_id, outgoing) in successors.into_iter().zip(outgoing_states) {
    // `outgoing` is cloned for all but the last successor; the last takes ownership.
    // ... enqueue/propagate using `outgoing`
}
```

This standard helps teams make performance work defensible (measured) and efficient (no accidental cloning/extra layout cost).