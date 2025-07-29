---
title: Simplify configuration setup
description: Avoid redundant configuration parameters and prefer automated solutions
  over manual maintenance. Remove configuration options that duplicate library defaults,
  replace manual dependency lists with programmatic detection, and eliminate unused
  configuration logic when usage patterns change.
repository: remix-run/react-router
label: Configurations
language: JavaScript
comments_count: 4
repository_stars: 55270
---

Avoid redundant configuration parameters and prefer automated solutions over manual maintenance. Remove configuration options that duplicate library defaults, replace manual dependency lists with programmatic detection, and eliminate unused configuration logic when usage patterns change.

Key practices:
- Remove parameters that duplicate library defaults (e.g., `argv: process.argv.slice(2)` when it's already the default)
- Replace manual lists with automated detection where possible (e.g., `external: (id) => isBareModuleId(id)` instead of maintaining a hardcoded external dependencies array)
- Simplify configuration when requirements change (e.g., using `transformIgnorePatterns: []` instead of complex `modulePaths` setup)
- Clean up conditional logic and prompts that are no longer needed due to changed usage patterns

Example of improvement:
```javascript
// Before: Redundant and manual
let args = arg({}, { argv: process.argv.slice(2), stopAtPositional: true });
external: ["history", "@remix-run/router", "react", "react-dom"]

// After: Simplified and automated  
let args = arg({}, { permissive: true });
external: (id) => isBareModuleId(id)
```

This approach reduces maintenance burden, prevents configuration drift, and ensures setups work consistently across different environments and package managers.