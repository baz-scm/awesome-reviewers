---
title: Eliminate redundant code
description: Simplify code by eliminating redundancy and unnecessary complexity. This
  improves readability, reduces potential bugs, and makes the codebase easier to maintain.
repository: langchain-ai/langchainjs
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 15004
---

Simplify code by eliminating redundancy and unnecessary complexity. This improves readability, reduces potential bugs, and makes the codebase easier to maintain.

Some key practices to follow:

1. **Avoid unnecessary object creation**: Don't create objects that might be discarded immediately.
```typescript
// Instead of this:
let requestOptions: RequestOptions | undefined = {
  ...(config?.timeout ? { timeout: config.timeout } : {}),
  ...(config?.signal ? { signal: config.signal } : {}),
};

if (Object.keys(requestOptions).length === 0) {
  requestOptions = undefined;
}

// Do this:
const requestOptions: RequestOptions | undefined = config?.timeout || config?.signal
  ? { timeout: config.timeout, signal: config.signal }
  : undefined;
```

2. **Remove redundant await in returns**: In async functions, avoid using `await` when returning a promise.
```typescript
// Instead of this:
async function getData() {
  return await fetchData();
}

// Do this:
async function getData() {
  return fetchData();
}
```

3. **Use concise array methods**: Many array methods have default parameters you can omit.
```typescript
// Instead of this:
return embeddings.flat(1);

// Do this:
return embeddings.flat();
```

4. **Don't declare class properties only used in constructors**: If a property is only accessed inside the class constructor, it doesn't need to be a class property.
```typescript
// Instead of this:
class MyClass {
  json = false;
  
  constructor() {
    if (this.json) {
      // do something
    }
  }
}

// Do this:
class MyClass {
  constructor() {
    const json = false;
    if (json) {
      // do something
    }
  }
}
```

Eliminating redundancy leads to cleaner, more maintainable code that's easier to review and less prone to errors.
