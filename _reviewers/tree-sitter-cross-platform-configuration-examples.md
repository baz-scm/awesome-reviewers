---
title: Cross-platform configuration examples
description: Ensure configuration examples and documentation work across different
  operating systems and clearly distinguish between required and optional configuration
  steps. Avoid platform-specific syntax that may not work universally, and explicitly
  state when configuration steps are optional versus mandatory.
repository: tree-sitter/tree-sitter
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 21799
---

Ensure configuration examples and documentation work across different operating systems and clearly distinguish between required and optional configuration steps. Avoid platform-specific syntax that may not work universally, and explicitly state when configuration steps are optional versus mandatory.

When providing path examples in configuration files, use universally supported formats:
```json
{
  "parser-directories": [
    "~/src",
    "$HOME/dev",
    "/Users/my-name/code"
  ]
}
```

Use plain `~` instead of `~username` syntax, as the latter doesn't work on all systems. For optional build or setup steps, clearly indicate their optional nature and explain the implications of skipping them:

```md
Optionally, build the WASM library. If you skip this step, then the `tree-sitter web-ui` command will require an internet connection.
```

This prevents developers from encountering platform-specific failures and helps them make informed decisions about which configuration steps to include in their setup.