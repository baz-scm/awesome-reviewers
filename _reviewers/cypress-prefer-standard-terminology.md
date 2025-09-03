---
title: Prefer standard terminology
description: Use widely accepted industry-standard names and conventions rather than
  descriptive but non-standard alternatives. This improves code readability and maintainability
  by leveraging established terminology that developers are already familiar with.
repository: cypress-io/cypress
label: Naming Conventions
language: JSX
comments_count: 2
repository_stars: 48850
---

Use widely accepted industry-standard names and conventions rather than descriptive but non-standard alternatives. This improves code readability and maintainability by leveraging established terminology that developers are already familiar with.

For components, prefer established UI terminology over descriptive names:
```jsx
// Avoid descriptive but non-standard names
const UiBlocker = () => { /* ... */ }

// Prefer widely accepted industry terms  
const Scrim = () => { /* ... */ }
```

For file extensions, use standard conventions consistently:
```
// Prefer standard extensions for new files
CollapseIcon.tsx  // instead of CollapseIcon.jsx
```

This approach reduces cognitive load for developers who can immediately understand the purpose and behavior based on familiar naming patterns from the broader development community.