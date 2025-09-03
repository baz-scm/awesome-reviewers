---
title: Avoid hardcoded configuration values
description: Replace hardcoded values in configuration code with design tokens, parameters,
  or configurable constants to ensure consistency and maintainability across the codebase.
repository: ant-design/ant-design
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 95882
---

Replace hardcoded values in configuration code with design tokens, parameters, or configurable constants to ensure consistency and maintainability across the codebase.

When writing configuration-related code, avoid embedding magic numbers or fixed values directly. Instead, use design tokens for spacing, colors, and sizes, or make values configurable through parameters.

**Bad:**
```typescript
[`&-vertical`]: {
  display: 'flex',
  flexDirection: 'column',
  rowGap: 8,  // hardcoded value
  [`&${groupPrefixCls}-large`]: {
    rowGap: 12,  // hardcoded value
  },
}

// or
maxWidth: 'calc(100% - 4px)',  // hardcoded 4px
```

**Good:**
```typescript
[`&-vertical`]: {
  display: 'flex',
  flexDirection: 'column',
  rowGap: token.marginXS,  // use design token
  [`&${groupPrefixCls}-large`]: {
    rowGap: token.marginSM,  // use design token
  },
}

// or make it configurable
const mergedConfig = {
  ...contextConfig,
  ...userConfig,  // proper configuration merging
};
```

This approach ensures that configuration values remain consistent across components, can be easily updated globally through design tokens, and reduces the risk of inconsistencies when modifications are needed.