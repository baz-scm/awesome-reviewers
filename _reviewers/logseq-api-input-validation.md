---
title: API input validation
description: When working with APIs, always validate inputs beyond basic format checking
  to ensure semantic correctness and handle edge cases properly. Simple constructor
  calls or basic format validation may accept invalid or unexpected inputs that could
  cause issues downstream.
repository: logseq/logseq
label: API
language: TypeScript
comments_count: 3
repository_stars: 37695
---

When working with APIs, always validate inputs beyond basic format checking to ensure semantic correctness and handle edge cases properly. Simple constructor calls or basic format validation may accept invalid or unexpected inputs that could cause issues downstream.

For URL validation, don't rely solely on constructor success - verify the parsed components meet your requirements:

```typescript
const isValidURL = (url: string) => {
  try {
    const parsedUrl = new URL(url)
    return parsedUrl.host && ['http:', 'https:'].includes(parsedUrl.protocol)
  } catch {
    return false
  }
}
```

Similarly, when choosing API methods, understand their behavior and constraints rather than assuming functionality. Test different approaches empirically when stability is critical, and be prepared to revert changes if they break expected behavior. Always validate that your API usage works as intended across different scenarios and edge cases.