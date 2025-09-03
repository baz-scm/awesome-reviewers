---
title: Use semantically accurate names
description: Variable, method, and type names should precisely reflect their actual
  content, purpose, or scope. Names that misrepresent what they contain or do create
  confusion and make code harder to understand and maintain.
repository: ChatGPTNextWeb/NextChat
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 85721
---

Variable, method, and type names should precisely reflect their actual content, purpose, or scope. Names that misrepresent what they contain or do create confusion and make code harder to understand and maintain.

Ensure that:
- Type names match their actual structure (use `PartialLocaleType` for partial implementations, not the full `LocaleType`)
- Variable names correspond to their context (use `const no: LocaleType` for Norwegian locale, not `const en: LocaleType`)
- Parameter purposes are clear through naming and explicit defaults

Example of problematic naming:
```typescript
// Misleading - suggests full locale but may be partial
import { LocaleType } from "./index";

// Confusing - Norwegian locale named as English
const en: LocaleType = {
  // Norwegian translations...
};
```

Example of semantically accurate naming:
```typescript
// Clear - indicates partial implementation
import { PartialLocaleType } from "./index";

// Accurate - matches the actual locale
const no: LocaleType = {
  // Norwegian translations...
};

// Explicit default parameter
export function getHeaders(ignoreHeaders: boolean = false) {
  // ...
}
```

This practice makes code self-documenting and reduces cognitive load when reading and maintaining the codebase.