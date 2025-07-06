---
title: Make errors user actionable
description: 'Error messages should provide clear, actionable information that helps
  users understand and resolve the problem. Each error should:

  1. Include specific context about what failed'
repository: astral-sh/uv
label: Error Handling
language: Rust
comments_count: 6
repository_stars: 60322
---

Error messages should provide clear, actionable information that helps users understand and resolve the problem. Each error should:
1. Include specific context about what failed
2. Explain why it failed
3. When applicable, suggest how to fix it

Example of improving error messages:

```rust
// Instead of:
#[error(transparent)]
ManagedPythonError(#[from] managed::Error),

// Prefer:
#[error("Failed to discover managed Python installations")]
ManagedPythonError(#[from] managed::Error),

// Even better with context and remedy:
#[error("Failed to authenticate with {url}")]
#[error("hint: Check your credentials or configure authentication using UV_INDEX_{index}_USERNAME")]
AuthenticationError { url: String, index: String }
```

When designing error handling:
- Use specific error variants instead of returning Ok(None) for expected failure cases
- Include relevant context (URLs, file paths, version numbers) in error messages
- Add hints or help messages for common failure scenarios
- Distinguish between different failure modes (e.g., missing vs invalid credentials)
- Keep error messages focused on the user's perspective rather than internal implementation details