---
title: optimize component memoization
description: When implementing React.memo for performance optimization, ensure props
  are structured to enable effective memoization. Pass individual primitive props
  separately rather than complex objects to allow React.memo to correctly detect unchanged
  props and prevent unnecessary re-renders.
repository: calcom/cal.com
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 37732
---

When implementing React.memo for performance optimization, ensure props are structured to enable effective memoization. Pass individual primitive props separately rather than complex objects to allow React.memo to correctly detect unchanged props and prevent unnecessary re-renders.

Example:
```tsx
// Before - complex object prop prevents effective memoization
<FormBuilderField field={{ ...field, hidden }} readOnly={readOnly} />

// After - individual props enable React.memo optimization  
<MemoizedField field={field} hidden={hidden} readOnly={readOnly} />
```

This approach is particularly important in components that render frequently or contain expensive operations. Consider the performance impact of data fetching patterns as well - avoid duplicate API calls by leveraging client-side query caching or strategic prop passing when the same data is needed in multiple components.