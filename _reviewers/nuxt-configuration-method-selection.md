---
title: Configuration method selection
description: Choose the appropriate configuration method based on when values are
  needed and whether they can change at runtime. Use `runtimeConfig` for values that
  need to be set via environment variables after build (especially secrets), `app.config`
  for public build-time configuration that won't change, and `process.env` only in
  server contexts when outside the Nuxt...
repository: nuxt/nuxt
label: Configurations
language: Markdown
comments_count: 6
repository_stars: 57769
---

Choose the appropriate configuration method based on when values are needed and whether they can change at runtime. Use `runtimeConfig` for values that need to be set via environment variables after build (especially secrets), `app.config` for public build-time configuration that won't change, and `process.env` only in server contexts when outside the Nuxt framework.

Key guidelines:
- `runtimeConfig`: Private or public tokens that need to be specified after build using environment variables
- `app.config`: Public tokens determined at build time, for website configuration such as theme variant, title, and any project configuration that is not sensitive  
- `process.env`: Only use in server contexts outside Nuxt framework (like `nuxt.config.ts` at build time)

Remember that `nuxt.config.ts` only runs at build time, so you cannot change anything in it using environment variables at runtime (including runtimeConfig).

```ts
// nuxt.config.ts - build time only
export default defineNuxtConfig({
  runtimeConfig: {
    // Private keys (only available on server-side)
    apiSecret: process.env.API_SECRET,
    // Public keys (exposed to client-side)
    public: {
      apiBase: process.env.API_BASE_URL || '/api'
    }
  }
})

// app.config.ts - build time, public values
export default defineAppConfig({
  theme: {
    primaryColor: '#ababab'
  },
  title: 'My App'
})

// In components/composables - runtime
const config = useRuntimeConfig()
const appConfig = useAppConfig()
```