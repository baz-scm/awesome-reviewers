---
title: Use precise networking terminology
description: When writing error messages or documentation related to network requests
  and cross-origin policies, use precise terminology that accurately describes the
  scope of the issue. Prefer "URL" over "domain" when the problem could involve any
  URL component (protocol, port, path, etc.), not just the domain name. Use proper
  technical terms like "origin" when...
repository: cypress-io/cypress
label: Networking
language: Other
comments_count: 4
repository_stars: 48850
---

When writing error messages or documentation related to network requests and cross-origin policies, use precise terminology that accurately describes the scope of the issue. Prefer "URL" over "domain" when the problem could involve any URL component (protocol, port, path, etc.), not just the domain name. Use proper technical terms like "origin" when discussing same-origin policy violations.

For example, instead of:
```
A cross origin error happens when your application navigates to a new superdomain which does not match the origin policy above.
```

Use:
```
A cross origin error happens when your application navigates to a new URL which does not match the origin policy above.
```

This precision helps developers understand that the issue isn't limited to just domain changes but could involve protocol, port, or other URL components. Additionally, use proper grammar with articles ("a different origin" rather than "different origin") and hyphenate compound technical terms ("same-origin URLs") for clarity and consistency with web standards terminology.