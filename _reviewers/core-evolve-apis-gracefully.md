---
title: Evolve APIs gracefully
description: 'When modifying or extending APIs, prioritize backward compatibility
  while providing clear migration paths for future changes. Follow these practices:

  '
repository: vuejs/core
label: API
language: TypeScript
comments_count: 6
repository_stars: 50769
---

When modifying or extending APIs, prioritize backward compatibility while providing clear migration paths for future changes. Follow these practices:

1. **Mark deprecated APIs clearly** rather than removing them immediately:
```typescript
// Good: Keeping backward compatibility with clear deprecation notice
export const isGloballyAllowed = /*#__PURE__*/ makeMap(GLOBALS_ALLOWED)
/** @deprecated use `isGloballyAllowed` instead */
export const isGloballyWhitelisted = isGloballyAllowed
```

2. **Support both old and new parameters** by normalizing internally:
```typescript
// Good: Supporting both boolean and string namespace types
mount(
  rootContainer: HostElement | string,
  isHydrate?: boolean,
  namespace?: ElementNamespace | boolean // Support both forms
) {
  // Internally normalize boolean to string representation
  if (typeof namespace === 'boolean') {
    namespace = namespace ? 'svg' : undefined
  }
  // ...implementation
}
```

3. **Consider custom renderer implementations** when adding new methods to core interfaces, as they constitute breaking changes for implementers.

4. **Follow web standards** when implementing attribute behaviors, particularly for custom elements:
```typescript
// Following HTML spec for boolean attribute behavior
if (name === 'bar' && value === '') {
  // Treat empty string as true per HTML spec
  return true
}
```

5. **Use TypeScript interfaces** to enforce precise API contracts and accurately reflect browser behavior for event types and DOM interactions.

When uncertain about a change, consider adding a deprecation notice and providing the new approach in parallel rather than breaking existing code.