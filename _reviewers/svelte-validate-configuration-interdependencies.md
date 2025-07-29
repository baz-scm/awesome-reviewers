---
title: Validate configuration interdependencies
description: When configuration options have logical dependencies or constraints,
  implement both smart defaults and validation checks to ensure consistent behavior.
  Set dependent options to appropriate default values based on other configuration
  values, and validate that the final combination of options represents a valid state.
repository: sveltejs/svelte
label: Configurations
language: TypeScript
comments_count: 2
repository_stars: 83580
---

When configuration options have logical dependencies or constraints, implement both smart defaults and validation checks to ensure consistent behavior. Set dependent options to appropriate default values based on other configuration values, and validate that the final combination of options represents a valid state.

For interdependent options, derive defaults from related settings:
```typescript
options = assign({ 
  generate: 'dom', 
  dev: false, 
  shadowDom: options.customElement  // Default based on another option
}, options);
```

Then validate the final configuration to catch invalid combinations:
```typescript
if (!customElement && shadowDom) {
  throw new Error(`options.shadowDom cannot be true if options.customElement is false`);
}
```

This approach prevents invalid configuration states while maintaining backwards compatibility and providing clear error messages when constraints are violated.