---
title: consistent naming conventions
description: Maintain consistent naming patterns throughout your codebase, following
  established conventions and ensuring uniformity within the same context. This includes
  using correct syntax for configuration values, matching case conventions for related
  identifiers, organizing entries systematically (like alphabetically), and choosing
  descriptive names that clearly...
repository: helix-editor/helix
label: Naming Conventions
language: Toml
comments_count: 4
repository_stars: 39026
---

Maintain consistent naming patterns throughout your codebase, following established conventions and ensuring uniformity within the same context. This includes using correct syntax for configuration values, matching case conventions for related identifiers, organizing entries systematically (like alphabetically), and choosing descriptive names that clearly indicate purpose.

Examples of good practices:
- Use `underlined` instead of `underline` in modifier arrays to match the established API
- Match case conventions: use `selectionfg` consistently instead of mixing `selectionFG` and `selectionfg`
- Organize configuration entries alphabetically for better maintainability
- Choose descriptive file names like `hx_launcher.sh` instead of generic names like `hx`
- Use explicit long-form syntax like `[language-server.<name>]` for clarity

Inconsistent naming creates confusion, makes code harder to maintain, and can lead to subtle bugs when identifiers don't match their expected format.