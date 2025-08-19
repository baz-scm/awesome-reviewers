---
title: Use allowlists over blocklists
description: When filtering data for security purposes, prefer allowlists (explicitly
  defining what is permitted) over blocklists (explicitly defining what is forbidden).
  Blocklists are inherently less secure because they can miss new threats, require
  constant maintenance as infrastructure changes, and operate on the assumption that
  anything not explicitly blocked is...
repository: PostHog/posthog
label: Security
language: TypeScript
comments_count: 1
repository_stars: 28460
---

When filtering data for security purposes, prefer allowlists (explicitly defining what is permitted) over blocklists (explicitly defining what is forbidden). Blocklists are inherently less secure because they can miss new threats, require constant maintenance as infrastructure changes, and operate on the assumption that anything not explicitly blocked is safe.

Allowlists are more secure because they operate on the principle of least privilege - only explicitly permitted items are allowed, and everything else is automatically rejected. This approach is particularly important when handling user input, HTTP headers, API parameters, or any external data.

Example of converting from blocklist to allowlist for HTTP headers:

```ts
// Insecure: blocklist approach
const DISALLOWED_HEADERS = ['x-forwarded-for', 'x-forwarded-host', 'x-forwarded-proto', 'cookie']

// Secure: allowlist approach  
const ALLOWED_HEADERS = ['Accept', 'Accept-Encoding', 'Accept-Language', 'Cache-Control', 'Pragma', 'Content-Type', 'Content-Length', 'Content-Encoding', 'Content-Language', 'User-Agent', 'Host', 'Date']
```

Apply this principle when filtering file extensions, API endpoints, database fields, configuration options, or any scenario where you need to control what data is processed or passed through your system.