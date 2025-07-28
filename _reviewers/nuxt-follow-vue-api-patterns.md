---
title: Follow Vue API patterns
description: Always prefer Vue's native APIs and follow official Vue patterns instead
  of creating custom implementations. This ensures better compatibility, maintainability,
  and consistency with the Vue ecosystem.
repository: nuxt/nuxt
label: Vue
language: TypeScript
comments_count: 5
repository_stars: 57769
---

Always prefer Vue's native APIs and follow official Vue patterns instead of creating custom implementations. This ensures better compatibility, maintainability, and consistency with the Vue ecosystem.

Key practices:
- Use Vue's native composables when available (e.g., `useId` from Vue instead of custom implementations)
- Follow Vue's official configuration structures and API changes from changelogs
- Match Vue Router's API patterns when creating similar functionality (e.g., exposing `useLink` composable)
- Use proper Vue type definitions without redundancy

Example of migrating from custom to native Vue API:
```typescript
// Before: Custom implementation
export function useId(key?: string): string {
  // Custom SSR-friendly ID generation logic...
}

// After: Use Vue's native API
import { useId as _useId } from 'vue'
export const useId = _useId
```

Example of following Vue Router patterns:
```typescript
// Expose useLink to match RouterLink behavior
export const NuxtLink = defineComponent({
  // ... component definition
  useLink: useNuxtLink, // Matches Vue Router's RouterLink.useLink pattern
})
```

This approach reduces maintenance burden, improves ecosystem compatibility, and ensures your components work seamlessly with Vue tooling and development experience.