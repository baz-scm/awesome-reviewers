---
title: Consistent semantic naming
description: 'Use consistent, specific, and semantically appropriate naming conventions
  throughout the codebase. When creating new identifiers:


  1. Check for existing patterns for similar concepts (e.g., use ''ascending/descending''
  for sort options to match existing UI components)'
repository: grafana/grafana
label: Naming Conventions
language: TypeScript
comments_count: 4
repository_stars: 68825
---

Use consistent, specific, and semantically appropriate naming conventions throughout the codebase. When creating new identifiers:

1. Check for existing patterns for similar concepts (e.g., use 'ascending/descending' for sort options to match existing UI components)
2. Choose specific descriptive names over general ones (e.g., 'exportDashboardImage' instead of 'dashboardImageSharing')
3. Use semantically appropriate formats (e.g., past tense verbs like 'image_downloaded' for analytics events)
4. Apply consistent patterns across similar entities (e.g., if dashboards use a certain branch naming pattern like `folder/${generateTimestamp()}`)

For example:

```typescript
// Instead of this:
builder.addRadio({
  path: 'reduceOptions.sort',
  settings: {
    options: [
      { value: SortWithReducer.None, label: 'None' },
      { value: SortWithReducer.Asc, label: 'A-Z' },
      { value: SortWithReducer.Desc, label: 'Z-A' },
    ]
  },
});

// Do this (for consistency with tooltip sorting):
builder.addRadio({
  path: 'reduceOptions.sort',
  settings: {
    options: [
      { value: SortWithReducer.None, label: 'None' },
      { value: SortWithReducer.Asc, label: 'Ascending' },
      { value: SortWithReducer.Desc, label: 'Descending' },
    ]
  },
});
```

This approach improves code readability, maintainability, and reduces cognitive load for developers navigating the codebase.