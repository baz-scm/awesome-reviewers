---
title: Use cross-platform build commands
description: Replace native shell commands in package.json scripts with cross-platform
  alternatives to ensure build consistency across different operating systems. Native
  commands like `rm -rf` fail on Windows, breaking CI/CD pipelines that run on mixed
  environments.
repository: bytedance/UI-TARS-desktop
label: CI/CD
language: Json
comments_count: 2
repository_stars: 18021
---

Replace native shell commands in package.json scripts with cross-platform alternatives to ensure build consistency across different operating systems. Native commands like `rm -rf` fail on Windows, breaking CI/CD pipelines that run on mixed environments.

Use tools like `shx` or `rimraf` instead of native shell commands:

```json
{
  "scripts": {
    // ❌ Not cross-platform compatible
    "clean": "rm -rf build",
    "build": "rm -rf dist && rslib build && chmod +x dist/*.js",
    
    // ✅ Cross-platform compatible
    "clean": "shx rm -rf build", 
    "build": "shx rm -rf dist && rslib build && shx chmod +x dist/*.js"
  }
}
```

This ensures your build scripts work reliably in CI/CD environments regardless of the underlying operating system, preventing deployment failures due to platform-specific command incompatibilities.