---
title: Prevent Secret Leakage
description: 'Apply strict trust boundaries to authentication/credential state:


  - **Reset per-request sensitive fields on reuse** (especially pooled request/contexts).
  Never let prior request overrides (keys, base URLs, auth headers) bleed into later
  requests.'
repository: maximhq/bifrost
label: Security
language: Go
comments_count: 10
repository_stars: 6862
---

Apply strict trust boundaries to authentication/credential state:

- **Reset per-request sensitive fields on reuse** (especially pooled request/contexts). Never let prior request overrides (keys, base URLs, auth headers) bleed into later requests.
- **Write-protect security-critical context keys.** Treat reserved/internal keys as framework-owned: plugins should not be able to set them via public setters. Use an internal-only bypass for framework methods.
- **Never persist redacted/masked placeholders as real secrets.** If an update payload contains a “masked preview” (redacted non-secret), require a non-empty stored counterpart; otherwise fail validation (400) instead of storing the placeholder.
- **Validate outbound targets that depend on credentials/config** to prevent SSRF (e.g., enforce HTTPS + allowlisted host patterns; validate again at dial time, not only at create time).

Example (masked placeholder preservation rule):
```go
// incoming may be a UI placeholder like "****"; treat it as non-secret.
if incomingVal.IsRedacted() && !incomingVal.IsFromSecret() {
    if storedVal == nil || !storedVal.IsSet() {
        return fmt.Errorf("masked preview requires stored value") // reject
    }
    incomingVal = *storedVal // preserve real secret
}
```

Also ensure pooled objects are cleaned:
```go
// before putting request back into a pool or before reusing it
req.ProviderOverride = nil // clear per-request overrides
```

These practices reduce the risk of credential corruption, SSRF, and cross-request authentication bypass—key failure modes in the security domain.