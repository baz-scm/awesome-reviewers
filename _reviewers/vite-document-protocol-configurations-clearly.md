---
title: Document protocol configurations clearly
description: When documenting network protocol configurations (TLS, HTTP/2, CORS),
  provide specific details about required options, default values, and explicit behavior.
  Avoid ambiguous terminology like "sufficient values" and instead specify exactly
  what options are needed and how different settings interact.
repository: vitejs/vite
label: Networking
language: Markdown
comments_count: 2
repository_stars: 74031
---

When documenting network protocol configurations (TLS, HTTP/2, CORS), provide specific details about required options, default values, and explicit behavior. Avoid ambiguous terminology like "sufficient values" and instead specify exactly what options are needed and how different settings interact.

For example, instead of writing:
```md
Enable TLS + HTTP/2. Note this downgrades to TLS only when the `server.proxy` option is also used.

The value is an options object passed to `https.createServer()`.
```

Prefer more explicit documentation with required parameters:
```md
Enable TLS + HTTP/2. The value is an [options object](https://nodejs.org/api/https.html#https_https_createserver_options_requestlistener) passed to `https.createServer()`.

Required options include `key`/`cert` or `pfx` for server identity. Using `server.proxy` will disable HTTP/2 while maintaining TLS support.
```

For default configuration values, include the actual implementation details as seen in the CORS example, which clearly specifies the regex pattern for allowed origins. This precision prevents confusion, reduces follow-up questions, and ensures developers can implement network features correctly and securely.