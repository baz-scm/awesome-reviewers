---
title: Precise documentation links
description: When creating error messages related to security, permissions, or access
  controls, always provide specific links to relevant documentation. Use query parameters,
  anchors, or other mechanisms to direct users to the exact section of documentation
  that addresses their issue, rather than linking to generic pages.
repository: vercel/turborepo
label: Security
language: Rust
comments_count: 1
repository_stars: 28115
---

When creating error messages related to security, permissions, or access controls, always provide specific links to relevant documentation. Use query parameters, anchors, or other mechanisms to direct users to the exact section of documentation that addresses their issue, rather than linking to generic pages.

For example, instead of:
```rust
#[error("Insufficient permissions to write to remote cache. Please verify that your role has write access for Remote Cache Artifact at https://vercel.com/docs/accounts/team-members-and-roles/access-roles/team-level-roles")]
```

Prefer:
```rust
#[error("Insufficient permissions to write to remote cache. Please verify that your role has write access for Remote Cache Artifact at https://vercel.com/docs/accounts/team-members-and-roles/access-roles/team-level-roles?resource=Remote+Cache+Artifact")]
```

Specific links reduce friction when users troubleshoot security-related problems and increases the likelihood they'll correctly address permission issues without requiring additional support.