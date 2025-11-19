---
title: avoid redundant CI operations
description: CI/CD processes should eliminate unnecessary repetition and redundant
  operations across projects and builds. This includes avoiding repeated warning messages,
  preferring template-based configurations over runtime string replacements, and ensuring
  operations are performed once at the appropriate level rather than repeatedly for
  each project.
repository: nrwl/nx
label: CI/CD
language: TypeScript
comments_count: 3
repository_stars: 27518
---

CI/CD processes should eliminate unnecessary repetition and redundant operations across projects and builds. This includes avoiding repeated warning messages, preferring template-based configurations over runtime string replacements, and ensuring operations are performed once at the appropriate level rather than repeatedly for each project.

Key practices:
- Show warnings once during the overall process (e.g., nx-release) rather than once per project
- Use template files for configuration instead of runtime string manipulation
- Structure build dependencies properly to avoid redundant transpilation steps

Example of the problem:
```typescript
// Avoid: Warning shown for every project
logger.warn(
  `Docker support is experimental. Breaking changes may occur and not adhere to semver versioning.`
);

// Better: Show warning once at the process level during nx-release
```

Example of preferred approach:
```typescript
// Instead of runtime string replacement logic
// Update the template at packages/node/src/generators/application/files/common/webpack.config.js__tmpl__
// This ensures consistent configuration without repeated processing
```

This approach reduces build times, minimizes log noise, and creates more maintainable CI/CD pipelines by eliminating unnecessary duplication of operations.