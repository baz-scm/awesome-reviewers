---
title: Complete accurate documentation
description: Documentation should provide complete, accurate guidance that doesn't
  mislead developers about correct usage patterns. Avoid documentation structures
  that suggest incorrect import paths or API usage, and ensure that configuration
  examples are accompanied by practical usage demonstrations.
repository: remix-run/react-router
label: Documentation
language: Json
comments_count: 2
repository_stars: 55270
---

Documentation should provide complete, accurate guidance that doesn't mislead developers about correct usage patterns. Avoid documentation structures that suggest incorrect import paths or API usage, and ensure that configuration examples are accompanied by practical usage demonstrations.

When documenting APIs or configurations, consider how the documentation structure itself might be interpreted by users. For example, avoid typedoc entry point configurations that create misleading nested structures suggesting incorrect import paths like `react-router/index` when the correct import is just `react-router`.

Additionally, when showing configuration setup (like TypeScript plugins), include concrete usage examples in the same context:

```typescript
// tsconfig.json - Configuration
{
  "plugins": [{ "name": "@react-router/dev" }]
}

// app/routes/example.tsx - Usage demonstration  
export default function ExampleRoute() {
  // Show actual usage of the plugin's types/features here
}
```

This ensures developers understand both how to configure tools and how to actually use the features they enable, preventing incomplete or confusing documentation.