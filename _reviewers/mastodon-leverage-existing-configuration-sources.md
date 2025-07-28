---
title: leverage existing configuration sources
description: When implementing configuration logic, prefer using built-in configuration
  mechanisms and existing framework parameters over creating custom configuration
  options. This reduces complexity, improves maintainability, and follows established
  patterns.
repository: mastodon/mastodon
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 48691
---

When implementing configuration logic, prefer using built-in configuration mechanisms and existing framework parameters over creating custom configuration options. This reduces complexity, improves maintainability, and follows established patterns.

Key principles:
- Use framework-provided configuration objects instead of passing custom parameters
- Leverage type inference from existing interfaces rather than explicit type annotations
- Simplify state management by avoiding context-specific parameters when a single configuration can serve multiple use cases
- Handle undefined configuration values consistently with existing error handling patterns

Example from plugin configuration:
```typescript
// Instead of passing custom parameters
export function MastodonThemes(projectRoot: string): Plugin {
  return {
    name: 'mastodon-themes',
    config: () => {
      // custom logic with projectRoot
    }
  }
}

// Leverage built-in config object
export function MastodonThemes(): Plugin {
  return {
    name: 'mastodon-themes',
    async config(userConfig) { // Type inferred from Plugin interface
      const root = userConfig.root || process.cwd();
      // Use framework-provided configuration
    }
  }
}
```

This approach reduces the API surface, eliminates redundant parameters, and ensures consistency with framework conventions.