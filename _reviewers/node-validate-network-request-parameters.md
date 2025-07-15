---
title: Validate network request parameters
description: 'Always validate and sanitize all network request parameters to prevent
  injection attacks. This includes:


  1. **URL validation**: Consider restricting URLs to trusted origins only (e.g.,
  localhost/loopback interfaces) to reduce the attack surface.'
repository: nodejs/node
label: Security
language: JavaScript
comments_count: 2
repository_stars: 112178
---

Always validate and sanitize all network request parameters to prevent injection attacks. This includes:

1. **URL validation**: Consider restricting URLs to trusted origins only (e.g., localhost/loopback interfaces) to reduce the attack surface.

```javascript
// Bad - No validation on URL source
fetch(url, { signal: controller.signal })

// Better - Restrict URLs to trusted origins
const urlObj = new URL(url);
if (!['localhost', '127.0.0.1', '::1'].includes(urlObj.hostname)) {
  throw new Error('URL must be a loopback address for security reasons');
}
fetch(url, { signal: controller.signal })
```

2. **Header/payload sanitization**: Validate inputs used in constructing HTTP requests to prevent request smuggling attacks. Check for control characters like `\r` and `\n` that could manipulate request boundaries.

```javascript
// Bad - No validation against control characters
let payload = `CONNECT ${requestHost}:${reqOptions.port} HTTP/1.1\r\n`;
if (auth) {
  payload += `proxy-authorization: ${auth}\r\n`;
}

// Better - Validate parameters to prevent request smuggling
function validateNoControlChars(value, name) {
  if (/[\r\n]/.test(value)) {
    throw new Error(`${name} contains invalid control characters`);
  }
  return value;
}
let payload = `CONNECT ${validateNoControlChars(requestHost, 'requestHost')}:${validateNoControlChars(reqOptions.port, 'port')} HTTP/1.1\r\n`;
if (auth) {
  payload += `proxy-authorization: ${validateNoControlChars(auth, 'auth')}\r\n`;
}
```

These practices help prevent server-side request forgery (SSRF), HTTP request smuggling, and other injection-based attacks.