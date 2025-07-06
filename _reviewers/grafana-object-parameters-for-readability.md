---
title: Object parameters for readability
description: When a function has 3 or more parameters, use object destructuring instead
  of positional arguments. This improves code readability by making parameter names
  explicit at call sites and making the function signature more maintainable as parameters
  are added or modified.
repository: grafana/grafana
label: Code Style
language: TSX
comments_count: 2
repository_stars: 68825
---

When a function has 3 or more parameters, use object destructuring instead of positional arguments. This improves code readability by making parameter names explicit at call sites and making the function signature more maintainable as parameters are added or modified.

**Instead of this:**
```typescript
export const wrapWithPluginContext = <T,>(
  pluginId: string,
  extensionTitle: string,
  Component: React.ComponentType<T>,
  log: ExtensionsLog
) => {
  // Implementation
}

// Call site
wrapWithPluginContext('my-plugin', 'My Extension', MyComponent, logger);
```

**Do this:**
```typescript
export const wrapWithPluginContext = <T,>({
  pluginId,
  extensionTitle,
  Component,
  log,
}: {
  pluginId: string;
  extensionTitle: string;
  Component: React.ComponentType<T>;
  log: ExtensionsLog;
}) => {
  // Implementation
}

// Call site
wrapWithPluginContext({
  pluginId: 'my-plugin',
  extensionTitle: 'My Extension',
  Component: MyComponent,
  log: logger,
});
```

This approach makes it immediately clear what each parameter represents, allows for future parameter additions without breaking existing call sites, and makes the code easier to read and maintain.