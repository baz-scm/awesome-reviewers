---
title: Maintain code consistency
description: 'Ensure consistency throughout the codebase by following established
  patterns for both UI components and code structure. Specifically:


  1. Use semantic color names and variables rather than hardcoded values to maintain
  theme consistency and facilitate future changes:'
repository: apache/airflow
label: Code Style
language: TSX
comments_count: 5
repository_stars: 40858
---

Ensure consistency throughout the codebase by following established patterns for both UI components and code structure. Specifically:

1. Use semantic color names and variables rather than hardcoded values to maintain theme consistency and facilitate future changes:

{% raw %}
```tsx
// Bad
<Button _hover={{ bg: "gray.800" }} bg="black" color="white" />

// Good
<Button _hover={{ bg: "bg.emphasized" }} bg="bg.panel" color="fg.default" />
```
{% endraw %}

2. Reuse existing UI components and patterns when introducing similar functionality. For example, use the same icon sets across related features to provide visual consistency:

```tsx
// When adding new toggle functionality, reuse icons from similar components
// Use the same expand/collapse icons as in ToggleGroups.tsx
```

3. Extract repeated code patterns, configurations, and format strings into constants or utility functions to ensure consistency and simplify maintenance:

```tsx
// Bad - Repeating format strings
dayjs(date).tz(selectedTimezone).format("YYYY-MM-DD HH:mm:ss.SSS")
dayjs(anotherDate).tz(selectedTimezone).format("YYYY-MM-DD HH:mm:ss.SSS")

// Good - Define a constant
const DATE_TIME_FORMAT = "YYYY-MM-DD HH:mm:ss.SSS";
dayjs(date).tz(selectedTimezone).format(DATE_TIME_FORMAT)
dayjs(anotherDate).tz(selectedTimezone).format(DATE_TIME_FORMAT)

// Better - Extract a utility function for complex patterns
// In datetimeUtils.ts
export const formatDateTime = (date) => dayjs(date).tz(selectedTimezone).format(DATE_TIME_FORMAT);
```

By following these practices, you'll create a more maintainable codebase where developers can easily understand and extend existing patterns.