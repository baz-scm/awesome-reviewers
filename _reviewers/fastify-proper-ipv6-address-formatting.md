---
title: "Proper IPv6 address formatting"
description: "When constructing URLs with IP addresses, ensure IPv6 addresses are properly formatted according to RFC standards by wrapping them in square brackets. This applies to all IPv6 addresses, not just specific cases like localhost. Additionally, use appropriate event handlers for network events that should only be handled once per connection."
repository: "fastify/fastify"
label: "Networking"
language: "JavaScript"
comments_count: 2
repository_stars: 34000
---

When constructing URLs with IP addresses, ensure IPv6 addresses are properly formatted according to RFC standards by wrapping them in square brackets. This applies to all IPv6 addresses, not just specific cases like localhost (::1). Additionally, use appropriate event handlers (`once` instead of `on`) for network events that should only be handled once per connection.

Code example for IPv6 address handling:
```javascript
// Incorrect - only handles a specific IPv6 address
const host = address.address === '::1' ? '[::1]' : address.address

// Correct - handles all IPv6 addresses according to RFC standards
const host = address.family === 'IPv6' ? `[${address.address}]` : address.address
```

Code example for proper event handling:
```javascript
// Incorrect - may cause multiple handlers to be registered
session.on('connect', function () {
  http2Sessions.add(session)
})

// Correct - ensures the handler is registered exactly once
session.once('connect', function () {
  http2Sessions.add(session)
})
```

Following these practices ensures compliance with RFC 3986 and RFC 2732 for URL formatting and prevents potential issues with network connection management.