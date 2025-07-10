---
title: Clear code examples
description: Documentation should include clear, actionable code examples that users
  can reliably follow. Avoid using ambiguous placeholders or variables that might
  be misinterpreted as literal code to copy-paste. When placeholder values must be
  used in examples, explicitly mark them and provide clear instructions for replacement.
repository: Homebrew/brew
label: Documentation
language: Markdown
comments_count: 6
repository_stars: 44168
---

Documentation should include clear, actionable code examples that users can reliably follow. Avoid using ambiguous placeholders or variables that might be misinterpreted as literal code to copy-paste. When placeholder values must be used in examples, explicitly mark them and provide clear instructions for replacement.

For example, instead of:

```sh
eval "${HOMEBREW_PREFIX}/bin/brew shellenv)"
```

Which implies the variable is already set, use one of these approaches:

```sh
# Option 1: Use clear placeholder markers
eval "<Homebrew prefix path>/bin/brew shellenv)"

# Option 2: Include explicit instructions
# Replace /opt/homebrew with your installation directory
eval "/opt/homebrew/bin/brew shellenv)"
```

Similarly, when linking to API methods or classes in documentation, ensure the links are accurate and properly formatted. Check that URLs don't use encoded characters unnecessarily, and test links to confirm they direct to the intended destination.

This practice helps prevent confusion, reduces support requests, and creates a better experience for developers following your documentation.