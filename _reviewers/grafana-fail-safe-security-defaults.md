---
title: Fail-safe security defaults
description: Always implement security features with fail-safe defaults that deny
  access or disable insecure functionality unless explicitly configured. When security-sensitive
  features must be available in development environments, add explicit environment
  checks to prevent their use in production.
repository: grafana/grafana
label: Security
language: Go
comments_count: 4
repository_stars: 68825
---

Always implement security features with fail-safe defaults that deny access or disable insecure functionality unless explicitly configured. When security-sensitive features must be available in development environments, add explicit environment checks to prevent their use in production.

For example, when allowing an insecure mode that might be needed during development:

```go
// GOOD: Only allow insecure mode in development environments
if cfg.AllowInsecure && cfg.Env == setting.Dev {
    // Enable insecure feature
}

// BAD: Allows insecure mode in any environment
if cfg.AllowInsecure {
    // Enable insecure feature
}
```

Similarly, when implementing authorization logic:
1. Always default to denying access when parameters are missing or invalid
2. Verify all possible permission paths before granting access (including parent/child relationships)
3. Make security assumptions explicit in comments

This approach prevents accidental security bypasses in production while still enabling necessary development features in appropriate environments.