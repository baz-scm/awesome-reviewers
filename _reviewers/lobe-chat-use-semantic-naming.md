---
title: Use semantic naming
description: Choose names that reflect purpose and meaning rather than visual appearance,
  position, or implementation details. This improves code clarity, supports internationalization,
  and makes the codebase more maintainable.
repository: lobehub/lobe-chat
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 65138
---

Choose names that reflect purpose and meaning rather than visual appearance, position, or implementation details. This improves code clarity, supports internationalization, and makes the codebase more maintainable.

Avoid positional or appearance-based names like `right`, `left`, `top` that break in different contexts (RTL languages, responsive layouts). Instead, use semantic names that describe the role or function.

Example:
```tsx
// ❌ Avoid positional naming
const useStyles = createStyles(({ css }) => ({
  right: css`
    display: flex;
  `,
}));

// ✅ Use semantic naming
const useStyles = createStyles(({ css }) => ({
  assistant: css`
    display: flex;
  `,
  user: css`
    display: flex;
  `,
}));

// ❌ Avoid generic labels
<Button title="润色中">Stop</Button>

// ✅ Use descriptive, context-aware labels  
<Button title="语音输入">Stop</Button>
```

This approach ensures your code works across different languages, layouts, and contexts while making the intent clear to other developers.