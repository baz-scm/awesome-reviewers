---
title: Clear descriptive naming
description: Choose names that clearly communicate intent without requiring mental
  gymnastics to understand. Avoid double negatives in variable names, maintain consistent
  naming patterns across the codebase, and ensure names accurately describe their
  purpose and context.
repository: cloudflare/workerd
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 6989
---

Choose names that clearly communicate intent without requiring mental gymnastics to understand. Avoid double negatives in variable names, maintain consistent naming patterns across the codebase, and ensure names accurately describe their purpose and context.

Key principles:
- **Avoid double negatives**: Instead of `pythonNoGlobalHandlers` requiring `!pythonNoGlobalHandlers`, use positive naming like `legacyGlobalHandlers`
- **Be descriptive and contextual**: Function names should clearly indicate what they do and include relevant context (e.g., `nodeCompatHttpServerHandler` instead of generic `registerFetchEvents`)
- **Maintain consistency**: If using `Module` as a parameter name throughout the codebase, stick with it consistently, or rename the type to `ModuleType` to allow lowercase `module` parameters

Example of improvement:
```typescript
// Avoid - requires double negative
export const pythonNoGlobalHandlers: boolean = !!compatibilityFlags.python_no_global_handlers;
if (!pythonNoGlobalHandlers) { ... }

// Prefer - clear positive naming
export const legacyGlobalHandlers: boolean = !compatibilityFlags.python_no_global_handlers;
if (legacyGlobalHandlers) { ... }
```