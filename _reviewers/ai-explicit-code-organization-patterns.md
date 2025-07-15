---
title: Explicit code organization patterns
description: 'Maintain clear and explicit code organization patterns by following
  these guidelines:


  1. Use explicit property visibility in classes:

  - Prefer public properties over getters/setters when no additional logic is needed'
repository: vercel/ai
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 15590
---

Maintain clear and explicit code organization patterns by following these guidelines:

1. Use explicit property visibility in classes:
- Prefer public properties over getters/setters when no additional logic is needed
- Use private fields (#) for truly internal state
- Only use protected when inheritance is a core design requirement

2. Keep imports and exports explicit:
- Avoid wildcard exports (export *)
- Import directly from source files rather than barrel files
- Control what gets exported from each module

Example:
```typescript
// ❌ Avoid
export * from './utils';
import { something } from './index';

class MyClass {
  private messages: Message[];
  getMessages() { return this.messages; }
}

// ✅ Better
export { generateId, parseConfig } from './utils';
import { something } from './something';

class MyClass {
  #internalState: string;
  messages: Message[]; // public property when no special handling needed
}
```

This pattern improves code maintainability, makes dependencies clear, and helps control your public API surface.