---
title: Scope-Safe Identifier Naming
description: When converting source names (props, keys, wrapper-derived identifiers)
  into generated identifiers, follow these rules to keep naming correct and stable.
repository: facebook/react#b13
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 251893
---

When converting source names (props, keys, wrapper-derived identifiers) into generated identifiers, follow these rules to keep naming correct and stable.

- **Preserve semantics when required by syntax/meaning**: If the original name is not a valid identifier (e.g. JSX `aria-label`), keep the original spelling at the call site and use a **quoted key** in destructuring.
- **Sanitize deterministically for JS identifiers**: Convert to a consistent JS-safe identifier form (e.g. camelCase + fallback prefix like `_`).
- **Guarantee uniqueness using the correct scope**: Don’t rely on partial deduplication (e.g. a `seen` set) if it can miss identifiers already in scope. Prefer the compiler’s scope-aware unique generator (e.g. `programContext.newUuid()` / equivalent) so generated names can’t collide.
- **Treat naming inference as a heuristic that needs tests**: If you infer meaning from naming patterns (e.g. “PascalCase means component” through wrappers), add tests for both **valid** and **false-positive** cases (e.g. `debounce(() => { useHook(); })`) and make the false-positive strategy explicit (keep simple heuristic vs configurable wrappers).

Example (hyphenated JSX prop -> safe identifier while preserving original):
```ts
function isHyphenatedJsxProp(originalName: string): boolean {
  return !isValidIdentifier(originalName) && /^[a-zA-Z_][\w.-]*$/.test(originalName);
}

// call site keeps `aria-label`, destructuring uses quoted key
// const { "aria-label": ariaLabel } = props;
```