---
title: Cross-platform configuration simplification
description: When writing configuration files and scripts, prioritize cross-platform
  compatibility while keeping configurations simple and maintainable. Use platform-aware
  tools like `run-script-os` for npm scripts that need platform-specific behavior,
  but prefer built-in solutions and global defaults over complex custom configurations.
repository: menloresearch/jan
label: Configurations
language: Json
comments_count: 4
repository_stars: 37620
---

When writing configuration files and scripts, prioritize cross-platform compatibility while keeping configurations simple and maintainable. Use platform-aware tools like `run-script-os` for npm scripts that need platform-specific behavior, but prefer built-in solutions and global defaults over complex custom configurations.

For npm scripts, combine similar platform commands when possible:
```json
{
  "scripts": {
    "version-restore": "run-script-os",
    "version-restore:darwin:linux": "jq --arg ver $(cat .version.bak) '.version = $ver' package.json > package.tmp && mv package.tmp package.json && rm .version.bak",
    "version-restore:win32": "node -e \"/* Windows-specific implementation */\""
  }
}
```

Avoid explicitly setting configuration properties that can use sensible defaults. Consider using native tools (like `node --watch`) instead of additional dependencies when they provide equivalent functionality. This reduces complexity, improves maintainability, and ensures consistent behavior across different development environments.