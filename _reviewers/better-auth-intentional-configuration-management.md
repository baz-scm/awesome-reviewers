---
title: Intentional configuration management
description: Configuration choices should be intentional, balancing production requirements
  with developer experience while keeping configuration logic centralized in dedicated
  files rather than embedded inline.
repository: better-auth/better-auth
label: Configurations
language: Json
comments_count: 2
repository_stars: 19651
---

Configuration choices should be intentional, balancing production requirements with developer experience while keeping configuration logic centralized in dedicated files rather than embedded inline.

When making configuration decisions:
- Move configuration logic from inline scripts to dedicated config files (e.g., biome.json, tsup.config.js)
- Consider the impact on debugging and development workflows, not just production optimization
- Separate development and production configurations when they serve different purposes

Example of moving from inline to centralized configuration:

```json
// Instead of inline filters in package.json:
"format": "biome format . --write && pnpm --filter @better-auth/svelte-kit-example format"

// Define filters in biome.json and use simple commands:
"format": "biome format . --write"
```

For build configurations, provide separate commands for development and production needs:

```json
{
  "scripts": {
    "build": "tsup --clean --dts",
    "build:prod": "tsup --clean --dts --minify"
  }
}
```

This approach ensures configurations are maintainable, discoverable, and support both development debugging and production requirements.