---
title: Graceful failure handling
description: Operations that can fail—especially those involving external resources,
  OS APIs, or untrusted/edge-case input—must never panic or leave the system in an
  inconsistent state. Validate inputs defensively (e.g., clamp/guard against zero-size
  or inverted ranges) and return a `Result` instead of letting arithmetic or assertions
  panic; on failure, log the problem...
repository: cline/cline#"><b>zze3729958
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 71067
---

Operations that can fail—especially those involving external resources, OS APIs, or untrusted/edge-case input—must never panic or leave the system in an inconsistent state. Validate inputs defensively (e.g., clamp/guard against zero-size or inverted ranges) and return a `Result` instead of letting arithmetic or assertions panic; on failure, log the problem and continue with reduced functionality rather than crashing the whole app. When a multi-step operation partially succeeds and a later step fails, roll back or clean up everything that was already acquired (killed processes, removed map entries, closed handles) before propagating the error, so failures don't leak resources or leave orphaned state. If a code path depends on undocumented or inconsistent platform behavior, don't try to force it to "mostly work"—remove it and fall back to the officially supported mechanism so behavior is predictable across environments.

Example (cleanup on a late failure):
```rust
let mut map = sessions.lock().unwrap();
map.insert(id.clone(), session);
drop(map);

if let Err(error) = spawn_reader_thread(id.clone(), sessions.clone()) {
    // Don't leave a dangling session if the thread never started.
    if let Some(mut session) = sessions.lock().unwrap().remove(&id) {
        let _ = session.killer.kill();
    }
    return Err(format!("Failed to start the terminal reader: {error}"));
}
```

Example (avoid panic on degenerate input):
```rust
fn clamp_window_bounds(window: Bounds, work_area: Bounds) -> Result<Bounds, String> {
    if work_area.right <= work_area.left || work_area.bottom <= work_area.top {
        return Err("work area has zero or negative size".into());
    }
    // ... safe clamping using widened integer types
    Ok(clamped)
}
```