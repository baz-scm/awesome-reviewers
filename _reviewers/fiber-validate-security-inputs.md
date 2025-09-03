---
title: Validate security inputs
description: Always validate security-critical inputs to prevent DoS attacks and injection
  vulnerabilities. Implement size limits, scheme restrictions, and format validation
  for user-controlled data that affects security mechanisms.
repository: gofiber/fiber
label: Security
language: Go
comments_count: 3
repository_stars: 37560
---

Always validate security-critical inputs to prevent DoS attacks and injection vulnerabilities. Implement size limits, scheme restrictions, and format validation for user-controlled data that affects security mechanisms.

Key practices:
- Set reasonable size limits (e.g., 4KB for cookie values) to prevent DoS through oversized inputs
- Validate URL schemes for security-sensitive operations (only allow http/https for proxies)
- Follow standard library patterns for input sanitization and validation
- Avoid logging sensitive input values that could be exploited

Example implementation:
```go
// Validate proxy URL scheme
pURL, err := urlPkg.Parse(proxyURL)
if err != nil {
    return err
}
if pURL.Scheme != "http" && pURL.Scheme != "https" {
    return errors.New("unsupported proxy scheme")
}

// Limit cookie value size to prevent DoS
func (c *DefaultCtx) sanitizeCookieValue(v string) string {
    const maxCookieSize = 4096 // 4KB limit
    if len(v) > maxCookieSize {
        // Log generic message without exposing value
        log.Warn("cookie value exceeds size limit, truncating")
        v = v[:maxCookieSize]
    }
    // Continue with sanitization...
}
```

This prevents common attack vectors while maintaining functionality and following security best practices established in standard libraries.