---
title: Balance test performance considerations
description: When writing tests, consider both thoroughness and execution time. For
  operations with significant overhead (like Python installations, downloads, or filesystem
  operations), it's acceptable to consolidate multiple assertions into a single test.
repository: astral-sh/uv
label: Testing
language: Rust
comments_count: 4
repository_stars: 60322
---

When writing tests, consider both thoroughness and execution time. For operations with significant overhead (like Python installations, downloads, or filesystem operations), it's acceptable to consolidate multiple assertions into a single test.

```rust
// Instead of separate tests for each scenario:
#[test]
fn install_transparent_patch_upgrade_uv_venv() {
    // Setup context only once
    let context = TestContext::new_with_versions(&["3.13"]);

    // Test installing a lower patch version
    uv_snapshot!(context.filters(), context.python_install().arg("3.12.9"), /* ... */);

    // Create a virtual environment with same context
    uv_snapshot!(context.filters(), context.venv().arg("-p").arg("3.12"), /* ... */);
    
    // Test version verification with same context
    uv_snapshot!(context.filters(), context.run().arg("python").arg("--version"), /* ... */);
    
    // Test installing a higher patch version without recreating the environment
    uv_snapshot!(context.filters(), context.python_install().arg("3.12.10"), /* ... */);
}
```

When using snapshot testing, be conscious of brittleness. Try to make snapshots robust against implementation details while capturing essential behavior. For variable outputs, use focused filtering rather than replacing the entire expected output, or consider conditional snapshots for significantly different cases.

Prefer specific assertions (like `.assert().success()`) over empty snapshots when testing specific properties, as they provide better failure messages and are less likely to break on minor implementation changes.