---
title: validate client inputs
description: Always validate and sanitize client-provided data on the server side
  before processing. Client-side data, including form inputs, query parameters, and
  request bodies, should never be trusted without proper validation as it can be easily
  manipulated by malicious users.
repository: TanStack/router
label: Security
language: Markdown
comments_count: 1
repository_stars: 11590
---

Always validate and sanitize client-provided data on the server side before processing. Client-side data, including form inputs, query parameters, and request bodies, should never be trusted without proper validation as it can be easily manipulated by malicious users.

This applies to all data sources from the client:
- Form data (including hidden fields)
- URL parameters
- Request headers
- JSON payloads

Example of proper server-side validation:

```typescript
const yourFn = createServerFn('POST', async (formData: FormData) => {
  const rawVal = formData.get('val');
  
  // Validate and sanitize the input
  if (typeof rawVal !== 'string' || !rawVal.trim()) {
    throw new Error('Invalid input: val must be a non-empty string');
  }
  
  const val = rawVal.trim();
  
  // Additional validation based on expected format
  if (!/^\d+$/.test(val)) {
    throw new Error('Invalid input: val must be numeric');
  }
  
  const numericVal = parseInt(val, 10);
  // Now safe to use numericVal
})
```

Never assume client data is safe or correctly formatted, even if your client-side code generates it correctly.