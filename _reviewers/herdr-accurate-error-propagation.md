---
title: Accurate Error Propagation
description: In error-prone paths, do not “pretend success.” Always make the failure
  mode explicit to callers, and ensure any returned/serialized status reflects what
  actually happened.
repository: ogulcancelik/herdr
label: Error Handling
language: Rust
comments_count: 5
repository_stars: 26924
---

In error-prone paths, do not “pretend success.” Always make the failure mode explicit to callers, and ensure any returned/serialized status reflects what actually happened.

Practical standards:
- Propagate unsupported/unsafe conditions as errors instead of silently falling back to a weaker contract.
- Treat partial/short/timeout outcomes as failures (or explicit “skipped” states), not success; retry only when it prevents a new safety issue.
- Prefer fail-closed for lifecycle/state invariants: if the guard mechanism can’t guarantee cleanup/correctness, return an error and leave the system in a safe state.
- Reject invalid input/state atomically: either process the whole batch or reject the whole batch, so you don’t apply out-of-context side effects.

Example (pattern to fix):
- If your API function waits with a timeout, return `bool`/`Result` and have the CLI fail when the target is still reachable after the timeout.

```rust
fn stop_session(name: Option<&str>) -> Result<SessionInfo, String> {
    let socket_path = api_socket_path_for(name);
    // ... send stop request ...

    // Must return whether the socket is actually stopped.
    let stopped = wait_until_stopped(&socket_path, STOP_WAIT_TIMEOUT)
        .map_err(|e| e.to_string())?;
    if !stopped {
        return Err(format!(
            "session {} did not stop within {:?} (still reachable at {})",
            name.unwrap_or(DEFAULT_SESSION_NAME),
            STOP_WAIT_TIMEOUT,
            socket_path.display()
        ));
    }

    Ok(session_info(name))
}
```

This standard prevents misleading “stopped”: true responses, avoids silent contract violations, and makes failures actionable for both users and automated tooling.