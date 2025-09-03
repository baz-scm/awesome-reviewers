---
title: Validate security configurations
description: Always verify that security middleware configurations use correct constant
  values, proper parameter specifications, and follow established security practices.
  Incorrect configuration values can create vulnerabilities or cause security features
  to fail silently.
repository: gofiber/fiber
label: Security
language: Markdown
comments_count: 5
repository_stars: 37560
---

Always verify that security middleware configurations use correct constant values, proper parameter specifications, and follow established security practices. Incorrect configuration values can create vulnerabilities or cause security features to fail silently.

Key areas to validate:
- Use framework-defined constants instead of string literals (e.g., `fiber.CookieSameSiteLaxMode` instead of `"Lax"`)
- Specify encryption key lengths correctly with proper AES algorithm mapping (16, 24, or 32 bytes for AES-128, AES-192, AES-256-GCM respectively)
- Understand the security implications of advanced features before implementation
- Ensure proper middleware ordering, especially placing encryption middlewares before those that read cookies

Example of proper CSRF configuration:
```go
app.Use(csrf.New(csrf.Config{
    CookieName:        "__Host-csrf_",
    CookieSecure:      true,
    CookieHTTPOnly:    true,
    CookieSameSite:    fiber.CookieSameSiteLaxMode, // Use constant, not "Lax"
    CookieSessionOnly: true,
    Extractor:         csrf.FromHeader("X-Csrf-Token"),
}))
```

Example of proper encryption key specification:
```go
// Generate 32-byte key for AES-256-GCM
key := encryptcookie.GenerateKey(32)
app.Use(encryptcookie.New(encryptcookie.Config{
    Key: key, // 32 bytes for AES-256-GCM
}))
```

This validation prevents security misconfigurations that could compromise application security or cause middleware to behave unexpectedly.