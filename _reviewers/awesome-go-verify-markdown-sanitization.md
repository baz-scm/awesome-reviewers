---
title: Verify markdown sanitization
description: When processing markdown content, always verify what sanitization your
  chosen markdown library provides to prevent XSS vulnerabilities while avoiding redundant
  security measures. Some libraries like `github_flavored_markdown` include built-in
  sanitization, while others like `blackfriday` require explicit sanitization of their
  output.
repository: avelino/awesome-go
label: Security
language: Go
comments_count: 2
repository_stars: 151435
---

When processing markdown content, always verify what sanitization your chosen markdown library provides to prevent XSS vulnerabilities while avoiding redundant security measures. Some libraries like `github_flavored_markdown` include built-in sanitization, while others like `blackfriday` require explicit sanitization of their output.

Before adding sanitization calls, check the library documentation to understand its security features. For libraries without built-in sanitization:

```go
// blackfriday requires explicit sanitization
body := string(blackfriday.MarkdownCommon(input))
sanitized := bluemonday.UGCPolicy().SanitizeBytes([]byte(body))
```

For libraries with built-in sanitization, avoid double-sanitization:

```go
// github_flavored_markdown already sanitizes - no additional sanitization needed
body := string(gfm.Markdown(input))
```

This prevents both security gaps from missing sanitization and performance issues from redundant sanitization calls.