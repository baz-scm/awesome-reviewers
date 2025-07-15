---
title: Precise CSP configuration
description: When integrating third-party services into your web application, carefully
  configure Content Security Policy (CSP) headers by explicitly specifying only the
  necessary domains for each directive. Understand the complete technical requirements
  of each service, including resources they might dynamically load. Add domains to
  appropriate directives based on how...
repository: prowler-cloud/prowler
label: Security
language: JavaScript
comments_count: 1
repository_stars: 11834
---

When integrating third-party services into your web application, carefully configure Content Security Policy (CSP) headers by explicitly specifying only the necessary domains for each directive. Understand the complete technical requirements of each service, including resources they might dynamically load. Add domains to appropriate directives based on how they're used (script-src, connect-src, img-src, etc.) to maintain strong security while preventing runtime CSP violations.

For example, when adding Google Tag Manager support:

```javascript
const cspHeader = `
  default-src 'self';
  script-src 'self' 'unsafe-inline' 'unsafe-eval' https://js.stripe.com https://www.googletagmanager.com;
  connect-src 'self' https://api.iconify.design https://api.simplesvg.com https://api.unisvg.com 
    https://js.stripe.com https://www.googletagmanager.com;
  img-src 'self' https://www.google-analytics.com https://www.googletagmanager.com;
  // Other directives...
`
```

This approach enhances security by following the principle of least privilege while ensuring functionality isn't broken by CSP violations. Document any non-obvious additions (like tracking pixels that might be injected by services) to help team members understand security decisions.