---
title: Explicit security parameters
description: Security-critical features should be implemented as required parameters
  rather than optional parameters or option functions. This forces developers to make
  explicit decisions about security settings, preventing accidental omissions that
  could introduce vulnerabilities.
repository: influxdata/influxdb
label: Security
language: Go
comments_count: 3
repository_stars: 30268
---

Security-critical features should be implemented as required parameters rather than optional parameters or option functions. This forces developers to make explicit decisions about security settings, preventing accidental omissions that could introduce vulnerabilities.

For example, when implementing authentication features like token hashing:

```go
// Good: Security parameter is required, must be explicitly set
func NewStore(ctx context.Context, kvStore kv.Store, useHashedTokens bool) (*Store, error) {
    // Implementation ensures token hashing is explicitly specified
}

// Risky: Security parameter could be accidentally omitted
func NewStore(ctx context.Context, kvStore kv.Store, opts ...StoreOption) (*Store, error) {
    // If WithHashedTokens option is forgotten, could create security vulnerability
}
```

This pattern ensures developers cannot accidentally omit critical security choices and makes security-relevant decisions more visible during code review. By making security parameters explicit, you enforce conscious decisions about security features rather than relying on defaults or optional configurations that might be overlooked.