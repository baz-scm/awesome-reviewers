---
title: Use proper HTTP utilities
description: When handling HTTP cookies and headers, use dedicated utility functions
  instead of manual string manipulation. Manual parsing of HTTP headers, especially
  cookies, can lead to incorrect behavior due to the complexity of HTTP header formats.
repository: nuxt/nuxt
label: Networking
language: Markdown
comments_count: 2
repository_stars: 57769
---

When handling HTTP cookies and headers, use dedicated utility functions instead of manual string manipulation. Manual parsing of HTTP headers, especially cookies, can lead to incorrect behavior due to the complexity of HTTP header formats.

For cookie handling, prefer established utilities like `splitCookiesString` from h3 or native browser APIs like `headers.getSetCookie()` over manual string splitting:

```ts
// ❌ Avoid manual cookie parsing
const cookies = (res.headers.get('set-cookie') || '').split(',')

// ✅ Use proper utilities
import { splitCookiesString } from 'h3'
const cookies = splitCookiesString(res.headers.get('set-cookie') || '')

// ✅ Or use native browser API
const cookies = res.headers.getSetCookie()
```

This approach ensures correct parsing of complex cookie values that may contain commas, semicolons, or other special characters that would break simple string splitting. Always verify that utility functions are available in your target environment before using them.