---
title: Clone network headers carefully
description: When working with HTTP or WebSocket headers in networking code, be cautious
  about header manipulation, cloning, and lifecycle management. Native headers in
  server implementations are often pooled and may be recycled after initial processing.
repository: spring-projects/spring-framework
label: Networking
language: Java
comments_count: 3
repository_stars: 58382
---

When working with HTTP or WebSocket headers in networking code, be cautious about header manipulation, cloning, and lifecycle management. Native headers in server implementations are often pooled and may be recycled after initial processing.

Specific considerations:
1. Preserve case-insensitivity of HTTP headers when copying them
2. For WebSocket handshakes, create a deep copy of headers as they may be needed after the original headers are recycled
3. Avoid adding duplicate headers when reading after headers are written

Example:
```java
// Incorrect - May lose case-insensitivity of header names
this.headers = new HttpHeaders(new LinkedMultiValueMap<>(original.getHeaders()));

// Correct - Create a proper copy that preserves HTTP header behavior
HttpHeaders headers = new HttpHeaders();
headers.addAll(request.getHeaders());
```

These practices help prevent subtle bugs related to header handling in network communication.