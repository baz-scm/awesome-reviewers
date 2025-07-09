---
title: Document configuration decisions
description: When modifying configuration files (package.json, tsconfig.json, etc.),
  document the reasoning behind significant changes and verify they don't introduce
  unexpected side effects. This is especially important for changes affecting dependencies
  and build processes.
repository: vercel/ai
label: Configurations
language: Json
comments_count: 3
repository_stars: 15590
---

When modifying configuration files (package.json, tsconfig.json, etc.), document the reasoning behind significant changes and verify they don't introduce unexpected side effects. This is especially important for changes affecting dependencies and build processes.

For dependency management:
- Use fixed versions when compatibility between related packages is critical
- Organize dependencies appropriately based on project type (internal tool vs. publishable library)

For build configurations:
- Follow best practices for your target environment
- Validate changes with thorough testing

Example:
```json
// package.json
{
  "dependencies": {
    // Fixed version for critical dependencies with compatibility requirements
    "prettier": "3.5.3",
    "prettier-plugin-svelte": "3.2.7",
    
    // Regular dependency for internal tools (not peer/dev)
    "zod": "3.23.8"
  }
}

// tsconfig.json
{
  "compilerOptions": {
    // Best practice for bundler targets (enables better dead code removal)
    "module": "ESNext",
    // Other settings...
  }
}
```

When making these changes, document your reasoning in commit messages or inline comments to provide context for other developers.