---
title: Accurate type signatures
description: 'When defining API interfaces in TypeScript, ensure that method signatures
  accurately reflect the actual behavior and requirements of the implementation. Pay
  special attention to:'
repository: aws/aws-sdk-js
label: API
language: TypeScript
comments_count: 2
repository_stars: 7628
---

When defining API interfaces in TypeScript, ensure that method signatures accurately reflect the actual behavior and requirements of the implementation. Pay special attention to:

1. Parameter optionality: Consider carefully whether parameters should be optional (`param?:`) or required based on their usage patterns. If a callback is expected to be called in most use cases, it might be better to make it required to guide developers toward correct usage.

2. Promise return types: Methods that return promises must specify the correct type of the resolved value. Never use `Promise<void>` when the promise actually resolves to a useful value.

Example of correcting return type:
```typescript
// Incorrect
getSignedUrlPromise(operation: string, params: any): Promise<void>;

// Correct 
getSignedUrlPromise(operation: string, params: any): Promise<string>;
```

Example of parameter optionality consideration:
```typescript
// With optional callback - allows but doesn't enforce callback usage
on(event: "validate", listener: (request: Request<D, E>, doneCallback?: () => void) => void): Request<D, E>;

// With required callback - enforces callback usage for correct implementation
on(event: "validate", listener: (request: Request<D, E>, doneCallback: () => void) => void): Request<D, E>;
```

Accurate type signatures improve API usability, enable better IDE support, and reduce runtime errors by catching incorrect usage patterns at compile time.
