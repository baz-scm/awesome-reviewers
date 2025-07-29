---
title: API naming consistency
description: Ensure related APIs use consistent naming patterns, parameter structures,
  and calling conventions across the codebase. When introducing new APIs alongside
  existing ones, maintain naming consistency to provide clarity and reduce cognitive
  load for developers.
repository: remix-run/react-router
label: API
language: Markdown
comments_count: 5
repository_stars: 55270
---

Ensure related APIs use consistent naming patterns, parameter structures, and calling conventions across the codebase. When introducing new APIs alongside existing ones, maintain naming consistency to provide clarity and reduce cognitive load for developers.

Key principles:
- Use consistent naming patterns for related functionality (e.g., `loaderData` and `actionData` instead of mixing `data` and `actionData`)
- Apply consistent calling conventions (e.g., if one configuration expects a function call like `routes()`, maintain that pattern)
- Use consistent formatting in documentation and changesets (e.g., backticks around API names: `createWorkersKVSessionStorage`)
- When deprecating APIs, provide clear migration paths with consistent naming in the replacement

Example of good consistency:
```ts
// Before: Inconsistent naming
interface RouteArgs {
  data: any;           // inconsistent with actionData
  actionData: any;
}

// After: Consistent naming  
interface RouteArgs {
  loaderData: any;     // consistent with actionData
  actionData: any;
}
```

This ensures developers can predict API patterns and reduces the learning curve when working with related functionality.