---
title: Precise Selection Logic
description: When implementing any selection algorithm (lookup/search/pick-next based
  on state or identifiers), make the selection rule precise and the state transitions
  intentional.
repository: ogulcancelik/herdr
label: Algorithms
language: Rust
comments_count: 2
repository_stars: 26924
---

When implementing any selection algorithm (lookup/search/pick-next based on state or identifiers), make the selection rule precise and the state transitions intentional.

- Avoid overly-broad predicates in matching/lookup: don’t use generic prefix/substring fallbacks unless the match set is explicitly constrained.
- Isolate side effects when the algorithm depends on history/state: only update history/auxiliary state for the specific branch where it logically changes.
- Lock behavior down with tests that cover both:
  - intended matches (positive cases)
  - near-miss/non-matches and history edge cases (negative/regression cases)

Example (explicit matching instead of broad prefix):
```rust
fn lookup_agent(name: &str) -> Option<Agent> {
    match name {
        "muse" | "muse-bin" | "muse-code" | "muse-cli" => Some(Agent::Muse),
        _ => None,
    }
}
```

Example (stateful selection: update history only when appropriate):
```rust
fn close_pane(&mut self, id: PaneId) {
    // Only touch focus/history if the closed pane is the currently focused one.
    if self.focus == id {
        // ... normal close behavior that updates focus
    }
    // If history points at the removed pane, clear it.
    if self.prev_focus == Some(id) {
        self.prev_focus = None;
    }
}
```

Apply this as a general algorithmic correctness checklist: define the exact predicate set for “what qualifies,” constrain fallbacks, prevent accidental overwrites of selection-related state, and add regression tests for the tricky edges that break determinism.