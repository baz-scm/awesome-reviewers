---
title: Explicit API Contracts
description: When API behavior depends on client/provider capabilities, request-field
  validity, or protocol ordering, implement it via explicit contracts—not heuristics—and
  ensure the exposed responses match the runtime’s effective configuration.
repository: aaif-goose/goose
label: API
language: Rust
comments_count: 10
repository_stars: 51876
---

When API behavior depends on client/provider capabilities, request-field validity, or protocol ordering, implement it via explicit contracts—not heuristics—and ensure the exposed responses match the runtime’s effective configuration.

Apply these rules:
1) Capability-first (no guessing). If the server needs client terminal/shell dialect, OS/execution context, or other environmental details, require them via a typed capability during initialization; keep server-local inference only as a backward-compatible fallback.
2) Schema-correct request emission. Only send provider-specific fields (or attachment shapes) to the endpoints/models that accept them. Prefer Option/guarded emission over “best effort” extra fields.
3) Normalize then expose. If you build a local ModelConfig/limits for an endpoint, ensure the returned API view matches what the runtime actually uses after provider normalization.
4) Stable machine semantics. For machine-readable modes, keep output purely structured; for human modes, separate prose from metadata. Ensure error/status/stop_reason are consistent.
5) Tests that pin ordering. When correctness relies on evaluation/handling order (e.g., deciding which error to return), add table-driven tests that lock the intended sequence.

Example pattern (capabilities + fallback):

```rust
// During initialize: client-provided typed capability
struct ClientCapabilities {
    // e.g. typed goose initialize metadata
    terminal_shell: Option<TerminalShellCapability>,
}

// On terminal/create: use capability; fallback only for legacy clients
fn terminal_shell_command(cap: &ClientCapabilities) -> (String, Vec<String>) {
    if let Some(c) = &cap.terminal_shell {
        (c.executable.clone(), c.args_prefix.clone())
    } else {
        // Backward-compatible fallback (server-owned)
        (server_default_shell(), vec![])
    }
}
```

Outcome: fewer cross-provider breakages, fewer “works in one mode” inconsistencies, and API responses that reliably reflect the behavior clients will observe at runtime.