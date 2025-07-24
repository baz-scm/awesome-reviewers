---
title: explicit authentication logic
description: Make authentication and security-related boolean conditions explicit
  and direct rather than using intermediate variables that obscure the logic. This
  improves code readability, reduces the risk of misconfiguration, and makes security
  decisions more auditable.
repository: prometheus/prometheus
label: Security
language: Go
comments_count: 1
repository_stars: 59616
---

Make authentication and security-related boolean conditions explicit and direct rather than using intermediate variables that obscure the logic. This improves code readability, reduces the risk of misconfiguration, and makes security decisions more auditable.

When configuring authentication settings, express the condition directly in the assignment rather than using intermediate boolean variables that add unnecessary complexity.

Example:
```go
// Instead of:
noAuth := true
if conf.ServiceAccountKey != "" || conf.ServiceAccountKeyPath != "" {
    noAuth = false
}
config := &Configuration{
    NoAuth: noAuth,
}

// Use direct boolean expression:
config := &Configuration{
    NoAuth: conf.ServiceAccountKey == "" && conf.ServiceAccountKeyPath == "",
}
```

This pattern makes the authentication logic immediately clear to reviewers and reduces the chance of introducing bugs through incorrect intermediate variable handling.