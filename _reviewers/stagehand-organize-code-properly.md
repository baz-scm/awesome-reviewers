---
title: organize code properly
description: Maintain clear code organization by placing code in appropriate files,
  directories, and modules. Respect module boundaries and create logical directory
  structures that reflect the code's purpose and domain.
repository: browserbase/stagehand
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 16443
---

Maintain clear code organization by placing code in appropriate files, directories, and modules. Respect module boundaries and create logical directory structures that reflect the code's purpose and domain.

Key principles:
- Place types in dedicated type files (e.g., move `StagehandInitResult` to `types/evals.ts`)
- Create domain-specific directories for related functionality (e.g., `lib/a11y` for accessibility utilities)
- Respect module boundaries (evals should reference `dist`, not `lib`)
- Group related functions in appropriately named files (prompts and prompt building functions belong in `prompts.ts`)

Example of proper organization:
```typescript
// Before: accessibility functions mixed in handlers
// lib/handlers/observeHandler.ts
type AccessibilityNode = { ... }
function formatSimplifiedTree() { ... }

// After: dedicated accessibility module  
// lib/a11y/utils.ts
type AccessibilityNode = { ... }
function formatSimplifiedTree() { ... }
```

This approach improves code discoverability, reduces coupling between modules, and makes the codebase easier to navigate and maintain.