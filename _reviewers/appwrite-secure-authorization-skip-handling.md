---
title: Secure authorization skip handling
description: When using authorization bypass mechanisms like `Authorization::skip()`,
  ensure proper security validation is maintained. Authorization skipping should only
  be used for internal system operations where the caller already has appropriate
  permissions, never for user-facing operations that require access control.
repository: appwrite/appwrite
label: Security
language: PHP
comments_count: 6
repository_stars: 51959
---

When using authorization bypass mechanisms like `Authorization::skip()`, ensure proper security validation is maintained. Authorization skipping should only be used for internal system operations where the caller already has appropriate permissions, never for user-facing operations that require access control.

Common pitfalls to avoid:
1. Don't skip authorization checks just to verify resource existence
2. Don't expose internal collection access through authorization bypasses
3. Ensure consistent authorization handling across related operations

Example of proper authorization handling:

```diff
- // BAD: Skips auth check entirely
- $database = Authorization::skip(fn () => 
-     $dbForProject->getDocument('databases', $databaseId)
- );
-
- if ($database->isEmpty()) {
-     throw new Exception(Exception::DATABASE_NOT_FOUND);
- }

+ // GOOD: Let DB layer handle authorization
+ try {
+     $database = $dbForProject->getDocument('databases', $databaseId);
+     
+     if ($database->isEmpty()) {
+         throw new Exception(Exception::DATABASE_NOT_FOUND);
+     }
+ } catch (AuthorizationException $e) {
+     // Convert to generic error to avoid information disclosure
+     throw new Exception(Exception::USER_UNAUTHORIZED);
+ }
```

Only use `Authorization::skip()` when:
- Accessing internal system collections that don't have user-level permissions
- Performing privileged operations where authorization was already verified
- Working with metadata that shouldn't block access to the main resource

Always document why authorization skipping is necessary and safe in that specific context.