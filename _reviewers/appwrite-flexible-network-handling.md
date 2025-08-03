---
title: Flexible network handling
description: When working with network connections and HTTP requests, implement flexible
  configuration patterns and robust response handling to prevent flaky behavior and
  ensure compatibility across environments.
repository: appwrite/appwrite
label: Networking
language: JavaScript
comments_count: 2
repository_stars: 51959
---

When working with network connections and HTTP requests, implement flexible configuration patterns and robust response handling to prevent flaky behavior and ensure compatibility across environments.

**For network configurations:**
- Always specify complete endpoint information including port numbers
- Use environment variables for configurable network settings

```javascript
// Instead of:
baseUrl: 'http://localhost', // May cause connection issues

// Use:
baseUrl: process.env.CYPRESS_BASE_URL || 'http://localhost:80', // Configurable with explicit port
```

**For HTTP response handling:**
- Accept all valid status codes for a given scenario rather than requiring a specific one
- Consider cache-related status codes (like 304) alongside traditional success codes

```javascript
// Instead of:
cy.wait('@request').its('response.statusCode').should('eq', 200)

// Use:
cy.wait('@request').its('response.statusCode').should('be.oneOf', [200, 304])
```

This approach accommodates legitimate response variations and different deployment environments, resulting in more reliable and maintainable network code.