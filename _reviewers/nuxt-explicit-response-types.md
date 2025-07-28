---
title: explicit response types
description: Always specify explicit response types when making API calls, especially
  for prerendered routes or external APIs. In production environments, response headers
  may not be preserved as expected, leading to incorrect content-type detection that
  can break applications in unpredictable ways.
repository: nuxt/nuxt
label: API
language: Markdown
comments_count: 5
repository_stars: 57769
---

Always specify explicit response types when making API calls, especially for prerendered routes or external APIs. In production environments, response headers may not be preserved as expected, leading to incorrect content-type detection that can break applications in unpredictable ways.

When fetching prerendered API routes, always set the `responseType` parameter:

```js
// Always specify responseType for prerendered routes
const articleContent = await $fetch('/api/content/article/name-of-article', {
  responseType: 'json'
})

// Also apply when using useFetch
const { data } = await useFetch('/api/data', {
  responseType: 'json'
})
```

Additionally, exercise extreme caution when proxying headers to external APIs. Only include headers you specifically need, as not all headers are safe to forward and may introduce unwanted behavior. This practice prevents content-type mismatches and ensures reliable API communication across different deployment environments.