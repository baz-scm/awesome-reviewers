---
title: Supported Interface Contracts
description: Define and honor the supported interface/contract for each platform and
  for each entry point. Don’t implement behavior that depends on unofficial, non-deterministic
  platform state; instead, constrain what you claim and provide explicit API/entry
  points for new request types.
repository: cline/cline#v19
label: API
language: Rust
comments_count: 2
repository_stars: 70885
---

Define and honor the supported interface/contract for each platform and for each entry point. Don’t implement behavior that depends on unofficial, non-deterministic platform state; instead, constrain what you claim and provide explicit API/entry points for new request types.

Apply this when designing startup/launch behavior or platform-specific “actions” (icons, activation, workspace selection, etc.):
- Confirm the platform-owned/guaranteed surfaces (what you can reliably control).
- Ensure your code and UI “promises” only the supported surface(s).
- Remove or avoid unsupported overrides when they can’t be made reliable across configurations.
- Treat launch/start semantics as an API contract: existing launch means “activate the running instance.”
- If you need to support additional request semantics (e.g., open a project path), introduce a dedicated future entry point like an `openPath`/`open this path` command rather than overloading argv/cwd forwarding.

Example pattern (single-instance + explicit future request):

```rust
tauri::Builder::default()
  // Existing launch contract: always activate the running instance
  .plugin(tauri_plugin_single_instance::init(|app, _argv, _cwd| {
    show_main_window(app);
  }))
  // Future: add a separate explicit API/entry point for open-path behavior
  // e.g., handle an `openPath` command/URI and route to workspace selection.
;
```

Outcome: more predictable behavior, fewer cross-platform inconsistencies, and clearer “API” boundaries between supported actions and future capabilities.