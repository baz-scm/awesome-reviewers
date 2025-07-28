---
title: Vue context boundaries
description: Ensure Vue composables, reactive state, and side effects are properly
  scoped within Vue's execution context to prevent SSR failures, memory leaks, and
  shared state across requests.
repository: nuxt/nuxt
label: Vue
language: Markdown
comments_count: 4
repository_stars: 57769
---

Ensure Vue composables, reactive state, and side effects are properly scoped within Vue's execution context to prevent SSR failures, memory leaks, and shared state across requests.

**Key Rules:**
1. **Never call composables at module top-level** - Composables must be called within `<script setup>`, `setup()` functions, or Vue lifecycle hooks where Nuxt context is available
2. **Avoid side effects in root scope** - Move timers, event listeners, and cleanup-requiring code into `onMounted` since unmount hooks don't run during SSR
3. **Don't define reactive state outside setup** - State defined outside component setup functions becomes shared across all users and requests

**Examples:**

❌ **Incorrect - Top-level composable usage:**
```ts
// utils/api.ts
const { session } = useUserSession() // Fails on server - no Nuxt context

export default defineNuxtPlugin((nuxtApp) => {
  // composable called outside proper context
})
```

❌ **Incorrect - Root scope side effects:**
```vue
<script setup>
// Timer in root scope - never cleaned up during SSR
const timer = setInterval(() => {}, 1000)

// Shared state across requests
export const myState = ref({})
</script>
```

✅ **Correct - Proper context usage:**
```ts
// utils/api.ts  
export default defineNuxtPlugin((nuxtApp) => {
  const { session } = useUserSession() // Called within plugin context
})
```

✅ **Correct - Side effects in lifecycle hooks:**
```vue
<script setup>
// Move side effects to mounted hook
onMounted(() => {
  const timer = setInterval(() => {}, 1000)
  
  onBeforeUnmount(() => {
    clearInterval(timer)
  })
})

// Use useState for proper SSR-safe state
const myState = useState('key', () => ({}))
</script>
```

This prevents SSR hydration mismatches, memory leaks, and ensures proper cleanup of resources across the Vue component lifecycle.