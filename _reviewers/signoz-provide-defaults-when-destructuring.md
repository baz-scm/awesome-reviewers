---
title: provide defaults when destructuring
description: When destructuring properties from objects that might contain undefined
  values, use the nullish coalescing operator (??) to provide explicit default values
  at the point of assignment. This prevents undefined values from propagating through
  your code and eliminates the need for repeated null checks later.
repository: SigNoz/signoz
label: Null Handling
language: TSX
comments_count: 2
repository_stars: 23369
---

When destructuring properties from objects that might contain undefined values, use the nullish coalescing operator (??) to provide explicit default values at the point of assignment. This prevents undefined values from propagating through your code and eliminates the need for repeated null checks later.

Instead of destructuring and handling nulls separately:
```tsx
const { showIP } = params;
// Later in code: showIP ?? true
```

Provide the default immediately:
```tsx
const showIP = params.showIP ?? true;
```

This pattern ensures that variables always have defined values, making your code more predictable and reducing the likelihood of null reference errors. Apply this approach consistently when accessing potentially undefined object properties, API responses, or configuration values.