---
title: Use 404 over 403
description: When blocking access to security-sensitive endpoints or directories,
  return HTTP 404 (Not Found) instead of 403 (Forbidden) to prevent information disclosure.
  A 403 response reveals that the resource exists but access is denied, which can
  provide valuable reconnaissance information to attackers. A 404 response makes it
  harder for attackers to determine what...
repository: mastodon/mastodon
label: Security
language: Other
comments_count: 1
repository_stars: 48691
---

When blocking access to security-sensitive endpoints or directories, return HTTP 404 (Not Found) instead of 403 (Forbidden) to prevent information disclosure. A 403 response reveals that the resource exists but access is denied, which can provide valuable reconnaissance information to attackers. A 404 response makes it harder for attackers to determine what resources are actually present on the server.

This principle applies to endpoints like certificate validation paths, admin interfaces, API endpoints, or any resource where revealing its existence could aid an attacker's reconnaissance efforts.

Example nginx configuration:
```nginx
# Instead of allowing discovery with 403
location /.well-known/acme-challenge/ { 
  deny all;  # This would return 403
}

# Use 404 to hide existence
location /.well-known/acme-challenge/ { 
  return 404;  # Appears as if path doesn't exist
}
```

Apply this pattern when the security benefit of hiding resource existence outweighs the need for clear error messaging.