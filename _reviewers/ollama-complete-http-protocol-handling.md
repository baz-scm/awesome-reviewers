---
title: Complete HTTP protocol handling
description: 'When implementing HTTP client functionality, ensure comprehensive support
  for all standard HTTP status codes and secure connection scenarios:


  1. Support all standard redirect status codes (301, 302, 303, 307, 308), not just
  a subset:'
repository: ollama/ollama
label: Networking
language: Go
comments_count: 2
repository_stars: 145705
---

When implementing HTTP client functionality, ensure comprehensive support for all standard HTTP status codes and secure connection scenarios:

1. Support all standard redirect status codes (301, 302, 303, 307, 308), not just a subset:

```go
switch resp.StatusCode {
case http.StatusOK:
    return requestURL, nil
case http.StatusMovedPermanently, // 301
     http.StatusFound,            // 302
     http.StatusSeeOther,         // 303
     http.StatusTemporaryRedirect, // 307
     http.StatusPermanentRedirect: // 308
    // Handle redirects
}
```

2. For HTTPS connections with self-signed or internal certificates, provide explicit mechanisms rather than general "insecure" flags. Consider using special URL schemes like `https+insecure://` for connections where certificate validation can be bypassed:

```go
if strings.HasPrefix(url, "https+insecure://") {
    // Configure TLS client to skip certificate validation
    tlsConfig.InsecureSkipVerify = true
    // Strip prefix for actual connection
    url = "https://" + url[16:]
}
```

3. Always document security implications when certificate validation is bypassed, with clear scope limitations (e.g., only for local development, internal networks).