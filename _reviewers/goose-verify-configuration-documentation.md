---
title: Verify configuration documentation
description: Ensure all configuration documentation accurately reflects actual system
  behavior, available options, and correct command syntax. Configuration errors in
  documentation lead to broken user setups and erode trust.
repository: block/goose
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 19037
---

Ensure all configuration documentation accurately reflects actual system behavior, available options, and correct command syntax. Configuration errors in documentation lead to broken user setups and erode trust.

Key areas to verify:
- **Command syntax**: Test that documented commands work as written (e.g., `goose session` not `goose session start`)
- **Feature availability**: Don't document configuration options that don't exist yet (like advanced container configuration that isn't implemented)
- **Parameter behavior**: Accurately describe how configuration parameters are inherited or passed (e.g., sub-recipes don't automatically inherit all parameters)
- **Command flags**: Verify correct flag usage (`cu version` vs `cu --version`)

Example of problematic documentation:
```bash
# Incorrect - this command doesn't exist
ALPHA_FEATURES=true goose session start

# Correct - verified working command  
ALPHA_FEATURES=true goose session
```

Before publishing configuration documentation, test each command and verify each described behavior actually works as documented. Remove or clearly mark any configuration options that are planned but not yet implemented.