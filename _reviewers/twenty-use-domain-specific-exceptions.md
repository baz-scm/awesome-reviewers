---
title: Use domain-specific exceptions
description: Create custom exception classes for each domain/module instead of throwing
  generic errors or letting applications crash. Include both technical details for
  developers and user-friendly messages for end users. Handle exceptions at the appropriate
  service layer rather than at API boundaries.
repository: twentyhq/twenty
label: Error Handling
language: TypeScript
comments_count: 6
repository_stars: 35477
---

Create custom exception classes for each domain/module instead of throwing generic errors or letting applications crash. Include both technical details for developers and user-friendly messages for end users. Handle exceptions at the appropriate service layer rather than at API boundaries.

Key principles:
- Define custom exception classes with specific error codes for each domain (e.g., `DnsManagerException`, `BillingException`, `ViewException`)
- Include `userFriendlyMessage` field for client-facing error communication
- Validate inputs early to prevent exceptions rather than catching them later
- Handle domain-specific exceptions at the service layer, not at GraphQL/controller layers
- Map technical exceptions to appropriate HTTP status codes when needed

Example:
```typescript
// Good: Domain-specific exception with user-friendly message
throw new DnsManagerException(
  'Hostname already registered',
  DnsManagerExceptionCode.HOSTNAME_ALREADY_REGISTERED,
  { userFriendlyMessage: 'Domain is already registered' },
);

// Bad: Generic error that crashes the application
throw new Error('More than one custom hostname found in cloudflare');

// Good: Validate before processing
if (!isDefined(fieldToDelete)) {
  throw new ViewException(
    'Field not found',
    ViewExceptionCode.FIELD_NOT_FOUND,
    { userFriendlyMessage: 'The field you are trying to delete does not exist' }
  );
}
```

This approach prevents application crashes, provides better debugging information, and enables graceful error handling throughout the application stack.