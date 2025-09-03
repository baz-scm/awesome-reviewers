---
title: Handle optional values safely
description: Always provide safe defaults or fallbacks when working with optional
  or potentially undefined values. Avoid using non-null assertion operators (`!`)
  on optional parameters, and ensure proper handling in type checking and value merging
  scenarios.
repository: ant-design/ant-design
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 95882
---

Always provide safe defaults or fallbacks when working with optional or potentially undefined values. Avoid using non-null assertion operators (`!`) on optional parameters, and ensure proper handling in type checking and value merging scenarios.

**Key practices:**
- Use default objects instead of non-null assertions: `val(info || { props: {} })` instead of `val(info!)`
- Order type checks to handle undefined cases first: check for object & not null, then boolean, then provide defaults
- Provide fallbacks for missing values: `color: var(--ant-tooltip-color, ${tooltipColor})` instead of assuming the CSS variable exists
- Skip undefined values in object merging to preserve existing values rather than overwriting with undefined

**Example:**
```typescript
// ❌ Dangerous - assumes info exists
return val(info!) as T;

// ✅ Safe - provides default
return val(info || { props: {} as Props }) as T;

// ❌ No fallback for missing CSS variable  
color: 'var(--ant-tooltip-color)',

// ✅ Provides fallback
color: `var(--ant-tooltip-color, ${tooltipColor})`,
```

This prevents runtime errors and ensures predictable behavior when dealing with optional or missing values.