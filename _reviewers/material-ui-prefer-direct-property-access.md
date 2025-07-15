---
title: Prefer direct property access
description: When property names are known at development time, use direct property
  access (e.g., `object.property`) over computed property access (e.g., `object[propertyName]`).
  This approach enhances code readability, enables better IDE autocompletion, improves
  type checking, and makes the code more maintainable.
repository: mui/material-ui
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 96063
---

When property names are known at development time, use direct property access (e.g., `object.property`) over computed property access (e.g., `object[propertyName]`). This approach enhances code readability, enables better IDE autocompletion, improves type checking, and makes the code more maintainable.

**Example - Instead of:**
```typescript
output[propName] = clsx(
  defaultProps?.[propName] as string,
  props?.[propName] as string,
);

output[propName] = {
  ...(defaultProps?.[propName] ?? ({} as React.CSSProperties)),
  ...(props?.[propName] ?? ({} as React.CSSProperties)),
};
```

**Prefer:**
```typescript
output.className = clsx(
  defaultProps.className,
  props.className,
);

output.style = {
  ...defaultProps.style,
  ...props.style,
};
```

This approach eliminates unnecessary dynamic property access, type assertions, and optional chaining when the property name is statically known. Code becomes more concise and the intent is clearer.