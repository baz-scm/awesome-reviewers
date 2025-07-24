---
title: Secure authentication flows
description: Design APIs with secure authentication flows by following proper error
  handling and documentation practices. Avoid non-null assertions in authorization
  code, properly document URL format requirements, and provide clear configuration
  steps for auth providers.
repository: supabase/supabase
label: API
language: Other
comments_count: 4
repository_stars: 86070
---

Design APIs with secure authentication flows by following proper error handling and documentation practices. Avoid non-null assertions in authorization code, properly document URL format requirements, and provide clear configuration steps for auth providers.

For authentication headers, handle potential null values safely:
```typescript
// Good: Handle potential null values safely
headers: { Authorization: req.headers.get('Authorization') }

// Bad: Using non-null assertion can lead to runtime errors
headers: { Authorization: req.headers.get('Authorization')! }
```

For redirect URLs, document format requirements explicitly:
```
// Important: Redirect URLs must end with a trailing slash
https://example.com/auth/callback/  // Correct
https://example.com/auth/callback   // May cause authentication failures
```

Remember to document all necessary provider configuration steps:
"Enable the provider you want to use under Auth Providers in the Supabase Dashboard and add the necessary credentials."