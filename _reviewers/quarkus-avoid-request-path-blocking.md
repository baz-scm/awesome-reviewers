---
title: Avoid request-path blocking
description: Minimize blocking operations in request-handling paths to ensure responsive
  application performance. Implement caching and asynchronous processing for expensive
  operations to reduce latency and improve throughput.
repository: quarkusio/quarkus
label: Performance Optimization
language: Other
comments_count: 3
repository_stars: 14667
---

Minimize blocking operations in request-handling paths to ensure responsive application performance. Implement caching and asynchronous processing for expensive operations to reduce latency and improve throughput.

When implementing APIs and services:

1. **Cache external service calls** to avoid repeated expensive operations. For authentication services like LDAP, enable caching to prevent roundtrips on every request:
```properties
quarkus.security.ldap.cache.enabled=true
```

2. **Use asynchronous operations** for tasks that could block requests. For example, configure asynchronous token refreshing instead of having clients wait during the request cycle:
```properties
# Configure asynchronous token refresh rather than blocking during requests
quarkus.oidc-client.async-refresh=true
```

3. **Choose efficient API methods** that avoid hidden performance costs. Select methods without unnecessary internal handlers or callbacks:
```java
// Less efficient: registers a reply handler internally
bus.requestAndForget("greeting", name)

// More efficient: direct send without handler overhead
bus.send("greeting", name)
```

Remember to consider the trade-offs: caching improves performance but introduces staleness (e.g., LDAP cache has a default max-age of 60s), while asynchronous operations add complexity but maintain responsiveness.