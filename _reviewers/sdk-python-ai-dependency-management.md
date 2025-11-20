---
title: AI dependency management
description: When integrating AI libraries and SDKs, carefully manage dependencies
  by pinning versions with upper bounds to prevent breaking changes and minimize scope
  by implementing simple types locally when possible.
repository: strands-agents/sdk-python
label: AI
language: Toml
comments_count: 2
repository_stars: 4044
---

When integrating AI libraries and SDKs, carefully manage dependencies by pinning versions with upper bounds to prevent breaking changes and minimize scope by implementing simple types locally when possible.

For version management, always specify upper bounds to avoid automatic consumption of breaking changes:
```toml
# Good: Pinned with upper bound
gemini = [
    "google-genai>=1.32.0,<2.0.0"
]

# Avoid: No upper bound
gemini = [
    "google-genai>=0.5.0"
]
```

For scope management, evaluate whether you truly need the full SDK or can implement simple components locally. Keep essential functionality like clients and error handling from the official SDK, but consider implementing basic types, enums, and configuration classes yourself to reduce dependency surface area. This approach balances functionality with dependency minimization while maintaining proper API communication and error handling.