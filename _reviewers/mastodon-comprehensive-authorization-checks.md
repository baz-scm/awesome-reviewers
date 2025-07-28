---
title: comprehensive authorization checks
description: Always implement thorough authorization checks at the earliest appropriate
  point in request processing, rather than relying solely on downstream filtering.
  This includes verifying user permissions, access rights, and relationship constraints
  (such as blocking status) before granting access to resources.
repository: mastodon/mastodon
label: Security
language: JavaScript
comments_count: 2
repository_stars: 48691
---

Always implement thorough authorization checks at the earliest appropriate point in request processing, rather than relying solely on downstream filtering. This includes verifying user permissions, access rights, and relationship constraints (such as blocking status) before granting access to resources.

Even when additional filtering occurs at the message or data level, upfront authorization prevents unnecessary processing and provides clearer security boundaries. Consider all relevant access control factors including user relationships, privacy settings, and resource ownership.

Example from streaming access:
```javascript
case 'profile':
  if (!params.account_id) {
    reject(new RequestError('Missing account id parameter'));
    return;
  }
  
  // Add comprehensive authorization check
  if (isAccountBlocked(params.account_id, req.accountId)) {
    reject(new AuthenticationError('Access denied'));
    return;
  }
```

This approach prevents security gaps where authorization logic is incomplete or missing entirely, as seen in cases where only basic parameter validation occurs without proper permission verification.