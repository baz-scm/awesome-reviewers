---
title: Restrict server access
description: Always configure server security settings with explicit allowed lists
  rather than permissive values. Using `true` for settings like `server.allowedHosts`
  or `server.cors` creates serious security vulnerabilities by allowing any website
  to access your development server through DNS rebinding attacks, potentially exposing
  source code and sensitive content.
repository: vitejs/vite
label: Security
language: Markdown
comments_count: 3
repository_stars: 74031
---

Always configure server security settings with explicit allowed lists rather than permissive values. Using `true` for settings like `server.allowedHosts` or `server.cors` creates serious security vulnerabilities by allowing any website to access your development server through DNS rebinding attacks, potentially exposing source code and sensitive content.

```js
// INSECURE: Don't do this
export default defineConfig({
  server: {
    allowedHosts: true,  // Allows any host to access your server
    cors: true  // Allows any origin to make requests
  }
})

// SECURE: Do this instead
export default defineConfig({
  server: {
    allowedHosts: ['myapp.local', '.example.com'],  // Only specific hosts
    cors: {
      origin: ['https://trusted-site.com']  // Only specific origins
    }
  }
})
```

Only add domains you control to these allowlists, and never add Top-Level Domains like `.com`. This protection is especially important for development servers where authentication might be disabled or less restrictive.