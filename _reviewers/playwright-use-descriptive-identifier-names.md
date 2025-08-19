---
title: Use descriptive identifier names
description: Choose specific, descriptive names for variables, methods, types, and
  other identifiers that clearly communicate their purpose and behavior. Avoid generic
  names, unnecessary abbreviations, and assumptions about usage context.
repository: microsoft/playwright
label: Naming Conventions
language: TypeScript
comments_count: 10
repository_stars: 76113
---

Choose specific, descriptive names for variables, methods, types, and other identifiers that clearly communicate their purpose and behavior. Avoid generic names, unnecessary abbreviations, and assumptions about usage context.

**Key principles:**
- Method names should accurately reflect their behavior and scope (e.g., `_allNativeContexts` instead of `_allContexts` when the method only returns native contexts)
- Use descriptive type names instead of generic ones (e.g., `InstalledBrowserInfo` instead of `Options`)
- Avoid abbreviations in favor of clarity (e.g., `typedArrayConstructors` instead of `typedArrayCtors`)
- Choose unique, specific names to prevent conflicts (e.g., `alreadyRegistered` instead of `foo`)
- Don't assume specific use cases in naming (e.g., avoid `getAllByAria` if it's not exclusively for aria purposes)

**Example:**
```typescript
// Avoid generic or abbreviated names
type Options = { ... };  // ❌ Too generic
const typedArrayCtors = { ... };  // ❌ Unnecessary abbreviation

// Use descriptive, specific names
type InstalledBrowserInfo = { ... };  // ✅ Clear purpose
const typedArrayConstructors = { ... };  // ✅ Full, clear name

// Method names should reflect actual behavior
_allContexts() { return this._browserTypes().flatMap(...); }  // ❌ Misleading scope
_allNativeContexts() { return this._browserTypes().flatMap(...); }  // ✅ Accurate scope
```

This approach improves code readability, reduces confusion, and makes the codebase more maintainable by ensuring identifiers clearly communicate their intended purpose.