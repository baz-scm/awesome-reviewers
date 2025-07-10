---
title: Use screen queries
description: When writing component tests, prefer using global `screen` queries from
  Testing Library instead of container-specific queries or passing query functions
  as parameters. This approach keeps the test environment simple and consistent across
  the codebase.
repository: mui/material-ui
label: Testing
language: TSX
comments_count: 2
repository_stars: 96063
---

When writing component tests, prefer using global `screen` queries from Testing Library instead of container-specific queries or passing query functions as parameters. This approach keeps the test environment simple and consistent across the codebase.

Instead of:
```typescript
const { container } = render(<TextareaAutosize style={{ backgroundColor: 'yellow' }} />);
const input = container.querySelector<HTMLTextAreaElement>('textarea')!;
```

Use:
```typescript
render(<TextareaAutosize style={{ backgroundColor: 'yellow' }} />);
const input = screen.getByRole('textbox');
```

Similarly, avoid passing query functions as parameters to test utilities when the global `screen` object can be used directly. This reduces complexity and follows the Testing Library's recommendation of using queries that resemble how users interact with your components.