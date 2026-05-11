---
title: Redact Transported Errors
description: When you serialize/dehydrate async results (queries, promises, RSC/RPC
  payloads), treat error objects as sensitive and do not transport raw server error
  details to the client/shared layer. Use a default redaction policy and make the
  behavior explicitly configurable and documented.
repository: tanstack/query
label: Security
language: TypeScript
comments_count: 2
repository_stars: 49380
---

When you serialize/dehydrate async results (queries, promises, RSC/RPC payloads), treat error objects as sensitive and do not transport raw server error details to the client/shared layer. Use a default redaction policy and make the behavior explicitly configurable and documented.

Apply this rule:
- Redact error message/stack (and any other sensitive fields) before dehydration/transport.
- Provide a single option/hook to control redaction (e.g., `shouldRedactError`) rather than hard-coding framework-specific assumptions.
- Decide and document how to handle special transport metadata (e.g., a `digest` field used for correlation): either preserve it intentionally for logging/correlation or redact it to prevent client exposure.

Example pattern:
```ts
function shouldRedactError(error: unknown): boolean {
  // default: redact to prevent leaking server-side details
  return true
}

function dehydratePromise(promise: Promise<unknown>) {
  return promise.catch((error) => {
    if (shouldRedactError(error)) throw new Error('redacted')
    throw error
  })
}
```
