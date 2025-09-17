---
title: Validate configuration assumptions
description: Before adding or modifying configuration settings, understand the underlying
  tool capabilities and test your assumptions. Many configuration issues arise from
  assumptions about what's needed without investigating whether the tool already provides
  the desired functionality or has specific constraints.
repository: microsoft/markitdown
label: Configurations
language: Json
comments_count: 2
repository_stars: 76602
---

Before adding or modifying configuration settings, understand the underlying tool capabilities and test your assumptions. Many configuration issues arise from assumptions about what's needed without investigating whether the tool already provides the desired functionality or has specific constraints.

For example, when setting up development containers, research whether build tools like Hatch already provide features you're trying to configure manually:

```json
// Instead of assuming you need postCreateCommand for editable installs
"postCreateCommand": "pip install -e .",

// Understand that Hatch already handles editable mode for testing
"features": {
    "ghcr.io/devcontainers-extra/features/hatch:2": {}
}
```

Similarly, when configuration choices seem to conflict with best practices (like using root user), document the practical constraints that necessitate the decision rather than just following defaults. Test alternative approaches when possible, but accept necessary trade-offs when tools have specific requirements for proper functionality.