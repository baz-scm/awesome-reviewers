---
title: improve code readability
description: Add line breaks and proper spacing between logical blocks within functions
  to improve code readability. When functions become complex with multiple logical
  sections, consider extracting nested logic into separate functions.
repository: nuxt/nuxt
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 57769
---

Add line breaks and proper spacing between logical blocks within functions to improve code readability. When functions become complex with multiple logical sections, consider extracting nested logic into separate functions.

For example, instead of cramped code:
```javascript
function uniquePlugins (plugins: NuxtPlugin[]) {
  const pluginFlags = new Set<string>()
  const bucket: NuxtPlugin[] = []
  for (const plugin of [...plugins].reverse()) {
    const name = plugin.name ? plugin.name : filename(plugin.src)
    const mode = plugin.mode ? plugin.mode : 'all'
    const flag = `${name}.${mode}`
    if (pluginFlags.has(flag)) {
      continue
    }
    pluginFlags.add(flag)
    bucket.push(plugin)
  }
  return bucket.reverse()
}
```

Use proper spacing between logical sections:
```javascript
function uniquePlugins (plugins: NuxtPlugin[]) {
  const pluginFlags = new Set<string>()
  const bucket: NuxtPlugin[] = []

  for (const plugin of [...plugins].reverse()) {
    const name = plugin.name ? plugin.name : filename(plugin.src)
    const mode = plugin.mode ? plugin.mode : 'all'
    const flag = `${name}.${mode}`

    if (pluginFlags.has(flag)) {
      continue
    }

    pluginFlags.add(flag)
    bucket.push(plugin)
  }

  return bucket.reverse()
}
```

Additionally, when complex logic can be extracted for better organization and readability, move it out of nested contexts into separate functions or higher-level scopes.