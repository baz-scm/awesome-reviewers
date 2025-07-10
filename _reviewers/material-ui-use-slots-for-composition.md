---
title: Use slots for composition
description: When designing React component APIs, implement the slots pattern using
  `slots` and `slotProps` props instead of specialized prop names. This approach provides
  a consistent, flexible, and maintainable way to customize component parts while
  preserving their functionality.
repository: mui/material-ui
label: React
language: Markdown
comments_count: 4
repository_stars: 96063
---

When designing React component APIs, implement the slots pattern using `slots` and `slotProps` props instead of specialized prop names. This approach provides a consistent, flexible, and maintainable way to customize component parts while preserving their functionality.

```jsx
// Instead of specialized props:
<SpeedDial actions={[
  { icon: <FileCopyIcon />, name: 'Copy', tooltipTitle: 'Copy' },
]} />

// Use slots pattern:
<SpeedDial actions={[
  { 
    icon: <FileCopyIcon />, 
    name: 'Copy', 
    slotProps: { tooltip: { title: 'Copy' } } 
  },
]} />
```

This pattern separates component structure from styling and behavior, making it easier to extend components without breaking changes. It creates a consistent API across your component library, improving developer experience and making your code more maintainable. When migrating components, consider replacing specialized props with the slots pattern to achieve greater flexibility and consistency.