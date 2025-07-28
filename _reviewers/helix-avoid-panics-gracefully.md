---
title: avoid panics gracefully
description: Replace panics, expects, and unwraps with graceful error handling that
  provides user feedback and allows the system to continue operating. Instead of crashing
  the application, log errors appropriately and return early or set status messages
  for the user.
repository: helix-editor/helix
label: Error Handling
language: Rust
comments_count: 4
repository_stars: 39026
---

Replace panics, expects, and unwraps with graceful error handling that provides user feedback and allows the system to continue operating. Instead of crashing the application, log errors appropriately and return early or set status messages for the user.

For example, instead of:
```rust
let config = debugger.config.clone();
let result = self
    .dap_servers
    .start_client(Some(socket), &config.expect("No config found"));
```

Use:
```rust
let config = match debugger.config.clone() {
    Some(config) => config,
    None => {
        log::error!("No config found for debugger");
        return true;
    }
};
let result = self.dap_servers.start_client(Some(socket), &config);
```

Similarly, replace panics with status line errors:
```rust
// Instead of: panic!("Expected non-empty argument roots.")
if roots.is_empty() {
    cx.editor.set_error("Expected non-empty argument roots");
    return;
}
```

This approach improves user experience by preventing crashes and providing meaningful feedback about what went wrong, while allowing the application to continue functioning.