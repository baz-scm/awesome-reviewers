---
title: Semantic Naming Safety
description: When code infers or transforms meaning based on identifier/naming rules,
  separate **syntactic validity** from **semantic intent** and prevent silent collisions/misclassification.
repository: facebook/react#b12
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 251896
---

When code infers or transforms meaning based on identifier/naming rules, separate **syntactic validity** from **semantic intent** and prevent silent collisions/misclassification.

Apply these rules:
1. **Preserve semantic names that can’t be safely converted to identifiers**: if an external name (e.g. JSX prop like `aria-label`) isn’t a valid JS identifier but is still valid in the source context, keep the original key and use a quoted key in destructuring.
2. **Sanitize only at the last responsible moment**: convert to a valid JS identifier only when you must bind to an identifier, using deterministic sanitization and collision-safe generation based on the correct deduplication boundary.
3. **Don’t over-rely on naming conventions for meaning**: if logic treats PascalCase as “component” (or similar), ensure wrapper/call-expression patterns can’t silently turn non-components into components. Add tests for edge wrappers and consider a configurable allowlist when inference is ambiguous.

Example (rule 1: quoted destructuring for non-identifier names):
```ts
function isHyphenatedJsxProp(originalName: string): boolean {
  return (
    !isValidIdentifier(originalName) && /^[a-zA-Z_][\w.-]*$/.test(originalName)
  );
}

// If originalName is like "aria-label", keep "aria-label" as the source key
// and destructure via a quoted key:
// const { "aria-label": ariaLabel } = props;
```

Test guidance:
- Include cases where naming/structure heuristics can be fooled (e.g., wrappers producing PascalCase assignments) and verify the behavior matches the intended semantic interpretation.