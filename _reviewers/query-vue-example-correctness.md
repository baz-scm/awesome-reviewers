---
title: Vue example correctness
description: When writing Vue (including Nuxt) code snippets or API docs, ensure the
  example is correct for the shapes the API truly supports and for the Nuxt/Vue environment.
repository: tanstack/query
label: Vue
language: Markdown
comments_count: 2
repository_stars: 49380
---

When writing Vue (including Nuxt) code snippets or API docs, ensure the example is correct for the shapes the API truly supports and for the Nuxt/Vue environment.

- For reactive inputs, don’t restrict types to a single form (e.g., only `Ref`). If the API accepts reactive values *and* getters/computed, type it accordingly (e.g., `MaybeRefOrGetter`) and normalize when you need an actual value.
- For Nuxt 3 snippets, import composables/helpers from the correct alias used by Nuxt auto-imports (typically `#imports`), so the snippet works when copied.

Example (typing + normalization for reactive inputs):
```ts
import { computed, type MaybeRefOrGetter, type Ref } from 'vue'
import { toValue } from 'vue'

function useTodos(todoId: MaybeRefOrGetter<string>) {
  const normalizedId: Ref<string> = computed(() => toValue(todoId))
  // ...use normalizedId.value where a plain string is needed
}
```

Nuxt 3 import alias (plugin/snippet correctness):
```ts
import { defineNuxtPlugin, useState } from '#imports'
```

This keeps docs precise and copy-pastable rather than only “almost correct” for real-world reactive inputs or Nuxt runtime resolution.