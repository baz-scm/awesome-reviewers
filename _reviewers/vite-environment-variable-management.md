---
title: Environment variable management
description: When working with environment variables in Vite applications, be explicit
  about variable loading behavior and precedence. Environment variables from `.env`
  files are always loaded regardless of mode, with mode-specific files (`.env.[mode]`)
  taking precedence over generic ones.
repository: vitejs/vite
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 74031
---

When working with environment variables in Vite applications, be explicit about variable loading behavior and precedence. Environment variables from `.env` files are always loaded regardless of mode, with mode-specific files (`.env.[mode]`) taking precedence over generic ones.

For type safety, use the TypeScript declaration merging pattern to strongly type your environment variables:

```typescript
/// <reference types="vite/client" />

// By adding this interface, you can make the type of ImportMetaEnv strict
// to disallow unknown keys.
interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  // more env variables...
}
```

When loading environment variables in config files, be explicit about which prefixes to include:

```javascript
import { defineConfig, loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  // Set the third parameter to 'APP_' to load envs with the `APP_` prefix.
  // If necessary, you can set the optional third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), 'APP_')

  return {
    // use env variables in config
    define: {
      'process.env.APP_ENV': JSON.stringify(env.APP_ENV)
    }
  }
})
```

To disable environment variable loading altogether, set `envDir: false` in your Vite config.