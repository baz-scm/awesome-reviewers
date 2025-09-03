---
title: JSDoc deprecation formatting
description: Ensure consistent formatting in JSDoc deprecation comments to improve
  API documentation clarity and developer experience. Use backticks around parameter/property
  names to distinguish them from regular text, use angle brackets for component names,
  and include "instead" for replacement suggestions.
repository: ant-design/ant-design
label: API
language: TSX
comments_count: 6
repository_stars: 95882
---

Ensure consistent formatting in JSDoc deprecation comments to improve API documentation clarity and developer experience. Use backticks around parameter/property names to distinguish them from regular text, use angle brackets for component names, and include "instead" for replacement suggestions.

**Format Guidelines:**
- Wrap parameter/property names in backticks: `parameterName`
- Use angle brackets for component names: `<ComponentName />`
- Include "instead" in replacement suggestions for clarity
- Avoid redundant explanations that the deprecation method already provides

**Examples:**

```typescript
// ✅ Good
/** @deprecated Please use `orientation` instead */
direction?: 'horizontal' | 'vertical';

/** @deprecated Please use `railColor` instead */
trailColor?: string;

// For components
warning.deprecated(
  true,
  '<Statistic.Countdown />',
  '<Statistic.Timer type="countdown" />',
);

// ❌ Bad  
/** @deprecated please use orientation */
/** @deprecated Please use trailColor instead */
/** @deprecated Please use `tabsPlacement` instead */ // Wrong parameter name
```

This standardization helps developers quickly identify deprecated APIs and their replacements, improving the overall API migration experience.