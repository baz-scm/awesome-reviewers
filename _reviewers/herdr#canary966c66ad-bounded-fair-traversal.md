---
title: Bounded fair traversal
description: When a search or traversal algorithm can encounter unbounded input (deep
  process trees, large directories, huge child lists), give it an explicit, finite
  work budget rather than letting it scan to completion. Favor streaming iteration
  (e.g., read_dir streamed one entry at a time) over materializing the full input
  into memory, and stop as soon as the budget...
repository: ogulcancelik/herdr#canary966c66ad
label: Algorithms
language: Rust
comments_count: 4
repository_stars: 46332
---

When a search or traversal algorithm can encounter unbounded input (deep process trees, large directories, huge child lists), give it an explicit, finite work budget rather than letting it scan to completion. Favor streaming iteration (e.g., read_dir streamed one entry at a time) over materializing the full input into memory, and stop as soon as the budget is exhausted or one element past what the caller needs to decide an outcome, so a pathological input cannot blow up latency or memory.

When the traversal has multiple independent roots or frontiers competing for that shared budget (e.g., a process-group leader subtree and an unrelated shell subtree), do not walk them sequentially — a wide or deep first root can exhaust the whole budget and starve the others, silently reintroducing correctness bugs under load. Instead, advance each frontier in round-robin turns, charging only what each turn actually consumes back to the shared budget, and give each root its own sub-budget for sub-expansions (e.g., per-pid thread/child enumeration) so one pathological branch cannot consume another's enumeration allowance. Keep the traversal order deterministic and covered by regression tests that construct a lopsided input (one huge subtree, one small target subtree) and assert the target is still found within the bound.

Example shape for a shared-budget, round-robin BFS over multiple roots:
```rust
let mut frontiers: Vec<VecDeque<u32>> = roots.map(|r| VecDeque::from([r])).collect();
loop {
    let mut progressed = false;
    for frontier in &mut frontiers {
        if budget.exhausted() { return pids; }
        let Some(pid) = frontier.pop_front() else { continue };
        progressed = true;
        pids.push(pid);
        let mut turn = budget.turn(); // bounded slice, not the whole remaining budget
        for child in expand(pid, &mut turn) {
            frontier.push_back(child);
        }
        budget.charge(turn.consumed());
    }
    if !progressed { break; }
}
```
This keeps worst-case work bounded, avoids full materialization when only a prefix of the data is needed, and guarantees fairness between competing branches of the search.