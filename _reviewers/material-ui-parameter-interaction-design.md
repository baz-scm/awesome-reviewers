---
title: Parameter interaction design
description: Design APIs with clear parameter interactions and priority rules to create
  intuitive interfaces. When multiple parameters could affect the same behavior, establish
  and document a consistent priority order rather than making parameters conditionally
  required.
repository: mui/material-ui
label: API
language: TypeScript
comments_count: 2
repository_stars: 96063
---

Design APIs with clear parameter interactions and priority rules to create intuitive interfaces. When multiple parameters could affect the same behavior, establish and document a consistent priority order rather than making parameters conditionally required.

Consider this Modal component example:
```typescript
// Good: Clear parameter priority without conditional requirements
const resolvedContainer = disablePortal
  ? ((mountNodeRef.current ?? modalRef.current)?.parentElement ?? getDoc().body)
  : getContainer(container) || getDoc().body;
```

This approach gives `disablePortal` priority over `container` without requiring users to provide `container` when using `disablePortal`.

Avoid redundant type definitions when parameters are inherited. For example, don't redefine callbacks in component props if they're already defined in a hook that the component extends. Instead, rely on the type hierarchy to provide proper documentation and type checking:

```typescript
// Avoid: Redundant type definition
interface AutocompleteProps extends UseAutocompleteProps {
  // Already defined in UseAutocompleteProps
  onScrollToBottom?: (event: React.SyntheticEvent) => void;
}
```

Always document parameter interactions and priorities clearly in component and function API references to help developers understand the expected behavior.