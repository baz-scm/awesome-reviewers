---
title: documentation generation compatibility
description: 'When making code changes, ensure compatibility with documentation generation
  tools like JSDoc and TypeDoc. This includes: (1) Exporting types that should appear
  in generated documentation, (2) Avoiding duplicate exports across modules that can
  confuse documentation parsers, and (3) Formatting code examples appropriately for
  documentation rendering.'
repository: remix-run/react-router
label: Documentation
language: TypeScript
comments_count: 3
repository_stars: 55270
---

When making code changes, ensure compatibility with documentation generation tools like JSDoc and TypeDoc. This includes: (1) Exporting types that should appear in generated documentation, (2) Avoiding duplicate exports across modules that can confuse documentation parsers, and (3) Formatting code examples appropriately for documentation rendering.

For exports, make sure types intended for public API documentation are properly exported:
```ts
export type {
  AwaitProps,
  IndexRouteProps,
  LayoutRouteProps,
  MemoryRouterOpts, // Export so typedoc picks it up
}
```

For code examples in JSDoc, handle existing markdown formatting to prevent double-wrapping:
```ts
markdown += example.includes("```")
  ? `${example}\n\n`
  : `\`\`\`tsx\n${example}\n\`\`\`\n\n`;
```

When creating nested modules, update documentation generation scripts to handle the new structure and prevent conflicts from duplicate component names across modules.