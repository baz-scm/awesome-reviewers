---
title: validate configuration values
description: Always verify configuration values against official documentation and
  test across target platforms before committing. Invalid configuration values can
  cause build failures, runtime errors, or platform-specific issues that are difficult
  to debug.
repository: cline/cline
label: Configurations
language: Json
comments_count: 3
repository_stars: 48299
---

Always verify configuration values against official documentation and test across target platforms before committing. Invalid configuration values can cause build failures, runtime errors, or platform-specific issues that are difficult to debug.

Key validation practices:
- Check configuration values against official documentation (e.g., TypeScript lib options, VS Code settings)
- Test configurations on all target platforms, especially when using environment variables
- Avoid assumptions about default keybindings or environment-specific values
- Use platform-agnostic paths and values when possible

Example of problematic configuration:
```json
// tsconfig.json - Invalid lib value
{
  "compilerOptions": {
    "lib": ["es2022", "esnext.disposable", "DOM"] // ❌ "esnext.disposable" is not valid
  }
}

// Fixed version
{
  "compilerOptions": {
    "lib": ["es2022", "DOM"] // ✅ Valid lib values only
  }
}
```

This prevents configuration-related build failures and ensures consistent behavior across development environments.