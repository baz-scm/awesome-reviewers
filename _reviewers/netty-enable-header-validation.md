---
title: Enable header validation
description: Always enable HTTP header validation to prevent request/response splitting
  vulnerabilities. These attacks can occur when untrusted data containing CRLF sequences
  is inserted into HTTP headers, allowing attackers to inject additional headers or
  even response body content.
repository: netty/netty
label: Security
language: Java
comments_count: 2
repository_stars: 34227
---

Always enable HTTP header validation to prevent request/response splitting vulnerabilities. These attacks can occur when untrusted data containing CRLF sequences is inserted into HTTP headers, allowing attackers to inject additional headers or even response body content.

When creating HTTP headers in Netty, avoid disabling the validation parameter:

```java
// INSECURE: Disabled header validation
HttpHeaders inHeaders = new DefaultHttpHeaders(false);

// SECURE: Keep validation enabled (default)
HttpHeaders inHeaders = new DefaultHttpHeaders(); 
// or explicitly
HttpHeaders inHeaders = new DefaultHttpHeaders(true);
```

Even in test code, prefer to use valid headers rather than disabling validation. If you absolutely must test with invalid headers, isolate this code and clearly document the security implications with comments.

Request/response splitting attacks can lead to cache poisoning, XSS, and session fixation. Modern browsers and servers have some protections against these attacks, but proper header validation remains an important security defense-in-depth measure.