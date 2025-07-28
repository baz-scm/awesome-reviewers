---
title: documentation formatting consistency
description: 'Ensure consistent formatting throughout documentation by applying these
  standards: wrap code terms, variable names, and boolean values in backticks (`data`,
  `error`, `status`, `true`, `false`), use proper markdown link syntax with leading
  slashes (`/docs/guide/...` instead of `docs/guide/...`), maintain consistent punctuation
  and spacing in code examples,...'
repository: nuxt/nuxt
label: Next
language: Markdown
comments_count: 16
repository_stars: 57769
---

Ensure consistent formatting throughout documentation by applying these standards: wrap code terms, variable names, and boolean values in backticks (`data`, `error`, `status`, `true`, `false`), use proper markdown link syntax with leading slashes (`/docs/guide/...` instead of `docs/guide/...`), maintain consistent punctuation and spacing in code examples, and fix syntax errors in code blocks.

Example of proper formatting:
```markdown
The `pending` object returned from `useAsyncData` is now a computed property that is `true` only when `status` is also pending.

See [route middleware](/docs/guide/directory-structure/middleware) for more details.

```vue
<template>
  <NuxtLink :to="{ name: 'posts-id', params: { id: 123 } }">
    Post 123
  </NuxtLink>
</template>
```

This consistency improves readability, ensures proper rendering of documentation, and provides a better developer experience when reading technical content.