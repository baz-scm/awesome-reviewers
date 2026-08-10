---
title: Effective Config Validation
description: When configuration has multiple sources (env vars, CLI flags, socket
  overrides) and/or platform-specific test compilation, treat only the *effective*
  configuration as authoritative.
repository: ogulcancelik/herdr
label: Configurations
language: Rust
comments_count: 3
repository_stars: 26924
---

When configuration has multiple sources (env vars, CLI flags, socket overrides) and/or platform-specific test compilation, treat only the *effective* configuration as authoritative.

Apply this standard:
- Precedence first: codify which source wins (e.g., CLI `--session` > `HERDR_SESSION` unless `HERDR_SOCKET_PATH` overrides socket selection).
- Validate conditionally: only validate/parse config values if they will actually be used. Don’t fail early on values that are overridden.
- Lock it with tests: add regression tests for precedence edge cases.
- Platform gating: if a module is already compile-gated for a target, avoid redundant per-test `#[cfg]`; if needed, gate at the narrowest helper/function scope.

Example (precedence regression shape):
```rust
// If no explicit --session is provided and HERDR_SOCKET_PATH is set,
// skip HERDR_SESSION validation because it is not authoritative.
#[test]
fn socket_path_wins_over_invalid_session_env() {
    std::env::set_var("HERDR_SOCKET_PATH", "/tmp/herdr.sock");
    std::env::set_var("HERDR_SESSION", "bad/name");

    // invoke: `herdr workspace list` (or the function that reads config)
    // assert: command proceeds (no validation error), and uses /tmp/herdr.sock
}
```

This prevents confusing failures from overridden settings and keeps tests compiling cleanly across platforms.