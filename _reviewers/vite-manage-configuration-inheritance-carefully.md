---
title: Manage configuration inheritance carefully
description: 'When designing configuration systems, establish clear default values
  and inheritance patterns. Follow these principles:


  1. Set explicit defaults that can be overridden by frameworks and users'
repository: vitejs/vite
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 74031
---

When designing configuration systems, establish clear default values and inheritance patterns. Follow these principles:

1. Set explicit defaults that can be overridden by frameworks and users
2. Use helper functions for merging configurations that handle arrays and nested objects appropriately
3. Allow framework-level defaults to be overridden by user configurations
4. Document the configuration resolution order

Example:
```js
// Bad - Hard to override defaults
config.isSPA = true;

// Good - Allows framework and user overrides
config.isSPA ??= true;

// Bad - Direct object merge loses array handling
const merged = { ...defaults, ...userConfig };

// Good - Use helper that handles arrays and nested objects
const merged = mergeWithDefaults(defaults, userConfig);

// Good - Framework providing defaults while allowing user override
export function frameworkConfig(userConfig) {
  return mergeConfig({
    build: {
      minify: false
    },
    dev: {
      port: 3000
    }
  }, userConfig);
}
```

This approach ensures configuration values are predictable, maintainable, and properly documented while providing flexibility for both framework authors and end users.