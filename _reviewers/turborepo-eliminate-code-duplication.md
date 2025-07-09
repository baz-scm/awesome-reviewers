---
title: Eliminate code duplication
description: Avoid duplicating logic, patterns, or data across the codebase. When
  similar code appears in multiple places, extract it into reusable functions or methods.
repository: vercel/turborepo
label: Code Style
language: Rust
comments_count: 6
repository_stars: 28115
---

Avoid duplicating logic, patterns, or data across the codebase. When similar code appears in multiple places, extract it into reusable functions or methods.

Examples:

1. Extract duplicated logic to shared functions:
```rust
// Instead of this:
let turbo_json_path = self.repo_root.join_component(CONFIG_FILE);
let turbo_jsonc_path = self.repo_root.join_component(CONFIG_FILE_JSONC);

let turbo_json_exists = turbo_json_path.exists();
let turbo_jsonc_exists = turbo_jsonc_path.exists();

// Extract to a helper function:
fn root_turbo_json_path(repo_root: &AbsoluteSystemPath) -> (AbsoluteSystemPathBuf, bool) {
    // Implementation that can be reused
}
```

2. Remove redundant initialization:
```rust
// Instead of:
enabled: remote_cache_opts.enabled,
no_update_notifier: None, // Remote cache options don't include this
..Self::default()  // This already handles no_update_notifier

// Just use:
enabled: remote_cache_opts.enabled,
..Self::default()
```

3. Prefer borrowing over cloning when possible:
```rust
// Instead of:
let repo_root = self.repo_root.clone();

// Use borrowing:
let repo_root = &self.repo_root;
```

4. Break large complex methods into smaller ones with clear responsibilities:
```rust
// Instead of embedding this logic in a larger function:
let conflict = {
    let own_invalidator = get_invalidator();
    let mut authorative_write_map = self.authorative_write_map.lock().unwrap();
    // ... 30+ lines of conflict resolution logic
};

// Extract to a dedicated method:
fn check_write_conflict(&self, path: &Path) -> Result<(), Error> {
    // Extracted conflict resolution logic
}
```

Following these practices improves maintainability, reduces the chances of inconsistencies, and makes the codebase easier to test and understand.