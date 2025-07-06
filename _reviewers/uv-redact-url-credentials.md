---
title: Redact URL credentials
description: 'Always redact sensitive credentials in URLs before logging, displaying
  in error messages, or serializing to prevent accidental exposure of authentication
  information. Use dedicated wrapper types like `LogSafeUrl` that automatically handle
  credential redaction when displaying URLs:'
repository: astral-sh/uv
label: Security
language: Rust
comments_count: 7
repository_stars: 60322
---

Always redact sensitive credentials in URLs before logging, displaying in error messages, or serializing to prevent accidental exposure of authentication information. Use dedicated wrapper types like `LogSafeUrl` that automatically handle credential redaction when displaying URLs:

```rust
// INSECURE: Directly logging a URL with potential credentials
log::debug!("Processing URL: {}", url);

// SECURE: Using a wrapper that handles credential redaction
log::debug!("Processing URL: {}", LogSafeUrl::from(url));
```

Be consistent in your approach to credential redaction:
- For debugging purposes, replace credentials with asterisks to indicate their presence (e.g., "****")
- For persistent storage like lockfiles, remove credentials entirely

Apply redaction as early as possible in the code path to minimize the risk that future changes might accidentally expose credentials. When implementing redaction logic, clearly document which approach is used in different contexts to maintain security throughout the application.