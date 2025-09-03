---
title: Environment variable validation
description: Always validate environment variables with proper type checking, fallback
  values, and defensive handling to prevent runtime failures and unexpected behavior.
repository: cypress-io/cypress
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 48850
---

Always validate environment variables with proper type checking, fallback values, and defensive handling to prevent runtime failures and unexpected behavior.

Environment variables can be undefined, have incorrect types, or contain invalid values. Implement defensive validation patterns that ensure your application gracefully handles these scenarios:

```typescript
// Bad: Direct usage without validation
const timeout = +process.env.CYPRESS_VERIFY_TIMEOUT || 30000
const baseUrl = process.env.CYPRESS_DOWNLOAD_MIRROR

// Good: Defensive validation with proper fallbacks
const getVerifyTimeout = (): number => {
  const verifyTimeout = +(process.env.CYPRESS_VERIFY_TIMEOUT || 'NaN')
  
  if (_.isNumber(verifyTimeout) && !_.isNaN(verifyTimeout)) {
    return verifyTimeout
  }
  
  return 30000
}

const getBaseUrl = (): string => {
  const baseUrl = process.env.CYPRESS_DOWNLOAD_MIRROR
  
  if (!baseUrl?.endsWith('/')) {
    return baseUrl ? baseUrl + '/' : defaultBaseUrl
  }
  
  return baseUrl || defaultBaseUrl
}

// Remember: Environment variables are always strings
const forceColor = process.env.FORCE_COLOR === '0' // not === 0
```

Key principles:
- Always provide sensible default values
- Validate types and ranges for numeric environment variables  
- Remember that environment variables are always strings when passed between processes
- Use optional chaining and nullish coalescing for safer property access
- Consider implementing opt-out mechanisms for privacy-sensitive features using environment variables like `CYPRESS_CRASH_REPORTS`