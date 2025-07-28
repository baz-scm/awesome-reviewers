---
title: Validate operation permissions
description: Ensure appropriate permission checks are implemented before performing
  security-sensitive operations that access files, networks, or system resources.
  Different operation types require different permission validations, and the timing
  of these checks matters for security.
repository: denoland/deno
label: Security
language: Rust
comments_count: 4
repository_stars: 103714
---

Ensure appropriate permission checks are implemented before performing security-sensitive operations that access files, networks, or system resources. Different operation types require different permission validations, and the timing of these checks matters for security.

Key considerations:
- File operations accessing paths require write/read permission checks based on the operation type
- Operations using resource IDs (file descriptors) may already have permissions validated at resource creation time
- Special paths like UNC paths or device paths may require elevated permissions (--allow-sys)
- Network operations should validate permissions before credential forwarding
- Operations accessible only through specific subcommands may inherit broader permissions from their context

Example implementation:
```rust
#[op2]
pub fn op_node_database_backup(
  #[cppgc] source_db: &DatabaseSync,
  #[string] path: String,
  #[serde] options: Option<BackupOptions>,
) -> std::result::Result<(), SqliteError> {
  // Add write permission checks here for the target path
  // Since path can have different forms, check permissions accordingly
  let src_conn_ref = source_db.conn.borrow();
  // ... rest of implementation
}
```

Always verify that permission checks align with the security model of the operation and consider whether the check should occur at operation time or resource creation time.