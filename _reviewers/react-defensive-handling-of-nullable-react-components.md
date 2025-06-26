---
title: "Defensive Handling of Nullable React Components"
description: "When working with React components that may return null or undefined values, implement defensive coding patterns to prevent runtime errors and improve code reliability."
repository: "facebook/react"
label: "React"
language: "TypeScript"
comments_count: 2
repository_stars: 237000
---

When working with React components that may return null or undefined values, implement defensive coding patterns to prevent runtime errors and improve code reliability.

- Consume iterables that may contain null values into an intermediate array before spreading them into React components:

```typescript
// Potentially problematic - may cause runtime errors if items contains null
const items = [0, 1, 2, null, 4, false, 6];
return <MyComponent items={items} />;

// Safer approach - create intermediate array and then spread
const items = [0, 1, 2, null, 4, false, 6];
const itemValues = items.filter(item => item !== null); 
return <MyComponent items={itemValues} />;
```

- When accessing properties of React component props or state, verify the prop/state exists first or use defensive access patterns like optional chaining and nullish coalescing:

```typescript
// Risky - assumes arr1[0] exists and has a value property
const MyComponent = ({ arr1 }) => <div>{arr1[0].value}</div>;

// Safer with optional chaining and nullish coalescing
const MyComponent = ({ arr1 }) => <div>{arr1?.[0]?.value ?? 0}</div>;
```

Following these practices will improve the robustness of your React code and help static analysis tools correctly infer nullability.