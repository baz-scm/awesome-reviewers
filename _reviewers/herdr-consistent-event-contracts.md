---
title: Consistent Event Contracts
description: When a single user action or state transition can be reached via multiple
  entrypoints (e.g., tab close vs workspace close), the externally observable behavior
  (especially emitted events) must be consistent with the actual underlying changes.
repository: ogulcancelik/herdr
label: API
language: Rust
comments_count: 2
repository_stars: 26924
---

When a single user action or state transition can be reached via multiple entrypoints (e.g., tab close vs workspace close), the externally observable behavior (especially emitted events) must be consistent with the actual underlying changes.

Apply this rule:
1) Define the observable contract at the boundary: what events should be emitted, how many, and for which concrete entities.
2) Centralize the source of truth for the transition: have shared helpers return the set of actually-affected items (e.g., which workspaces were removed), and derive emitted events from that return value—not from the initiating request/target.
3) Avoid “partial” behavior fixes that only patch one call path; they can create contract inconsistencies between APIs.
4) If platform/library constraints make behavior inherently limited, document the limitation in the public contract so callers aren’t surprised.

Sketch of the preferred pattern for event consistency:
```rust
// shared helper: return exactly what was removed
fn close_selected_workspace(...) -> Vec<WorkspaceId> {
    // ... compute closure of groups ...
    // return all ids actually removed
}

// at each API entrypoint
let removed = close_selected_workspace(...);
for id in removed {
    emit_event("workspace.closed", id);
}
```

And for documented constraints:
- Keep the behavior, but explicitly document the boundary limitation (e.g., “targets the foreground queue” / “cross-app caveat”) in the contract so clients know what outcomes to expect.