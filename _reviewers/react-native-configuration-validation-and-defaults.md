---
title: Configuration validation and defaults
description: Always validate configuration structure before accessing properties and
  provide sensible defaults while preserving explicit user overrides. Configuration
  code should defensively check for the existence of nested properties and gracefully
  handle missing or malformed configuration.
repository: facebook/react-native
label: Configurations
language: JavaScript
comments_count: 7
repository_stars: 123178
---

Always validate configuration structure before accessing properties and provide sensible defaults while preserving explicit user overrides. Configuration code should defensively check for the existence of nested properties and gracefully handle missing or malformed configuration.

When implementing configuration logic:
1. **Validate structure before access** - Check that nested configuration objects exist before accessing their properties
2. **Provide meaningful defaults** - Implement sensible default behavior when configuration is missing or incomplete  
3. **Respect explicit overrides** - Allow users to explicitly disable automatic behavior by providing their own configuration
4. **Handle edge cases gracefully** - Consider scenarios where configuration might be partially defined or in unexpected formats

Example of problematic code:
```javascript
// Crashes when dependency.platforms is undefined
Object.keys(dependency.platforms).forEach(platform => {
  if (dependency.platforms[platform] == null) {
    notLinkedPlatforms.push(platform);
  }
});
```

Example of improved code:
```javascript
// Defensive validation before access
if (dependency.platforms) {
  Object.keys(dependency.platforms).forEach(platform => {
    if (dependency.platforms[platform] == null) {
      notLinkedPlatforms.push(platform);
    }
  });
}
```

For default vs explicit configuration:
```javascript
// Provide defaults but respect explicit user configuration
if (!config.watchFolders.some(folder => folder !== ctx.root)) {
  // Apply auto-detection only when user hasn't specified custom folders
  overrides.watchFolders = getWatchFolders(ctx.root);
}
```

This approach prevents runtime crashes from malformed configuration while maintaining flexibility for users to customize behavior when needed.