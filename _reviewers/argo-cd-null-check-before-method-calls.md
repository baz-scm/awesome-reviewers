---
title: null-check before method calls
description: Always verify that properties are not null or undefined before calling
  methods on them to prevent runtime errors. This is especially important when filtering,
  mapping, or processing arrays where some objects may have missing or undefined properties.
repository: argoproj/argo-cd
label: Null Handling
language: TSX
comments_count: 2
repository_stars: 20149
---

Always verify that properties are not null or undefined before calling methods on them to prevent runtime errors. This is especially important when filtering, mapping, or processing arrays where some objects may have missing or undefined properties.

When working with potentially null properties, add explicit null checks before accessing methods:

```typescript
// Unsafe - can throw if project is null/undefined
const newRepos = repos.filter(repo => repo.project.includes(project));

// Safe - checks for null/undefined first
const newRepos = repos.filter(repo => repo.project && repo.project.includes(project));

// For arrays, filter out null/undefined values before processing
const projectItems = projectValues
    .filter(project => project && project.trim() !== '')
    .map(project => ({
        title: project,
        action: () => this.setState({ projectProperty: project })
    }));
```

This pattern prevents "Cannot read property 'X' of null/undefined" errors and makes code more robust when dealing with optional or potentially missing data.