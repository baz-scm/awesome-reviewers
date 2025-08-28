---
title: Add explanatory comments
description: 'When code behavior, limitations, or implementation decisions are not
  immediately obvious from reading the code itself, add explanatory comments to clarify
  the reasoning and context. This is especially important for:'
repository: cloudflare/workerd
label: Documentation
language: TypeScript
comments_count: 4
repository_stars: 6989
---

When code behavior, limitations, or implementation decisions are not immediately obvious from reading the code itself, add explanatory comments to clarify the reasoning and context. This is especially important for:

- **API limitations and scope**: Document when functions or classes have restricted functionality or are not part of standard APIs
- **Implementation decisions**: Explain why certain approaches were chosen, especially when they might seem unusual
- **Disabled linting rules**: Always explain why specific linting rules are disabled
- **Placeholder or unused code**: Clarify the purpose of code that exists for compatibility but isn't functionally used

Example from the codebase:
```typescript
// @ts-expect-error TS2416 Types insist value is a Socket, but it's actually unknown
set connection(value: unknown) {
  // Note: #socket is not actually used for anything other than making 
  // the property available for compatibility
  this.#socket = value;
}

/* eslint-disable @typescript-eslint/no-deprecated */
// Disabling deprecated warnings for this.finished and other attributes 
// which are deprecated in types/node package but required for compatibility
```

This practice prevents confusion for future maintainers and helps reviewers understand the context behind implementation choices.