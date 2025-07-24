---
title: HTTP security headers
description: Ensure that HTTP security headers are properly implemented and documented
  to prevent web vulnerabilities such as cache poisoning, clickjacking, and content
  type sniffing attacks. Security headers should be explicitly added to API responses
  and web endpoints as defensive measures.
repository: prometheus/prometheus
label: Security
language: Markdown
comments_count: 1
repository_stars: 59616
---

Ensure that HTTP security headers are properly implemented and documented to prevent web vulnerabilities such as cache poisoning, clickjacking, and content type sniffing attacks. Security headers should be explicitly added to API responses and web endpoints as defensive measures.

When implementing security headers, consider headers like:
- `Vary: Origin` to prevent cache poisoning attacks
- `X-Content-Type-Options: nosniff` to prevent MIME type confusion
- `X-Frame-Options` or `Content-Security-Policy` to prevent clickjacking
- `Strict-Transport-Security` for HTTPS enforcement

Example from the codebase:
```
* [BUGFIX] API: Add HTTP `Vary: Origin` header to responses to avoid cache poisoning. #16008
```

Always document security-related changes clearly in changelogs and commit messages, specifying the vulnerability being addressed and the protective measure being implemented.