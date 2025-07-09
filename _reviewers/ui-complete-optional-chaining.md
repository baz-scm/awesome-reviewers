---
title: Complete optional chaining
description: When using optional chaining (`?.`), ensure that **all subsequent operations**
  in the chain are also protected from null/undefined values. A common mistake is
  only protecting the initial object access while leaving subsequent method calls
  or property accesses vulnerable.
repository: shadcn-ui/ui
label: Null Handling
language: TSX
comments_count: 3
repository_stars: 90568
---

When using optional chaining (`?.`), ensure that **all subsequent operations** in the chain are also protected from null/undefined values. A common mistake is only protecting the initial object access while leaving subsequent method calls or property accesses vulnerable.

**Problems to avoid:**

1. Unprotected method returns:
```typescript
// PROBLEMATIC: scrollSnapList() result is unprotected
api?.scrollSnapList().map(...)
```

2. Incorrect control flow with void returns:
```typescript
// PROBLEMATIC: OR operator doesn't work with void returns
onClick={() => onClickStep?.(index, setStep) || onClickStepGeneral?.(index, setStep)}
```

**Better approaches:**

1. Protect the entire chain:
```typescript
// BETTER: Both api and its method result are protected
api?.scrollSnapList()?.map(...)

// BEST: Add length check for extra safety
api?.scrollSnapList()?.length > 0 && api.scrollSnapList().map(...)
```

2. Use proper conditionals for control flow:
```typescript
// Option 1: Explicit conditional
onClick={() => {
  if (onClickStep) {
    onClickStep(index, setStep);
  } else {
    onClickStepGeneral?.(index, setStep);
  }
}}

// Option 2: Execute both with separate optional chaining
onClick={() => {
  onClickStep?.(index, setStep);
  onClickStepGeneral?.(index, setStep);
}}
```

Always trace through the entire chain of operations when working with potentially null/undefined values to ensure each step is properly protected.