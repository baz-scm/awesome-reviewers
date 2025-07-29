---
title: document configuration hierarchies
description: When documenting configuration options, clearly explain all available
  configuration levels and their precedence order. Many configuration options can
  be set globally, per-component, or dynamically, and users need to understand these
  different approaches.
repository: sveltejs/svelte
label: Configurations
language: Markdown
comments_count: 6
repository_stars: 83580
---

When documenting configuration options, clearly explain all available configuration levels and their precedence order. Many configuration options can be set globally, per-component, or dynamically, and users need to understand these different approaches.

Structure configuration documentation by listing all available methods in order of precedence:

```js
// Multiple ways to set configuration options:

// 1. Globally, via compilerOptions in svelte.config.js
export default {
  compilerOptions: {
    css: 'injected',
    a11y: {
      rules: {
        'label-has-associated-control': {
          labelComponents: ['CustomInputLabel'],
          controlComponents: ['CustomInput'],
          depth: 3
        }
      }
    }
  }
}

// 2. Dynamically, using build tool options
// (e.g., dynamicCompileOptions in vite-plugin-svelte)

// 3. Per-component, with svelte:options (overrides other methods)
<svelte:options css="injected" />
```

This approach helps developers understand their configuration choices and prevents confusion about which settings take precedence. Always include practical examples showing the actual syntax for each configuration level.