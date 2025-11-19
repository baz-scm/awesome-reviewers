---
title: externalize configuration values
description: Configuration values should be externalized from code and read from standard
  locations like package.json or environment variables. Implement environment-aware
  validation that fails fast in production when required configuration is missing,
  while providing sensible defaults for development environments.
repository: nrwl/nx
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 27518
---

Configuration values should be externalized from code and read from standard locations like package.json or environment variables. Implement environment-aware validation that fails fast in production when required configuration is missing, while providing sensible defaults for development environments.

For environment variables, validate required values at application startup:

```javascript
if (!process.env.NEXT_PUBLIC_ASTRO_URL) {
  // If we're building for production throw error as each env must set this value.
  if (process.env.NODE_ENV === 'production') {
    throw new Error(
      `The NEXT_PUBLIC_ASTRO_URL environment variable is not set. Please set it to the URL of the Astro site.`
    );
  }
  // For dev, default to the canary docs.
  else {
    process.env.NEXT_PUBLIC_ASTRO_URL = 'https://master--nx-docs.netlify.app';
  }
}
```

For scripts, read configuration from package.json or config files rather than hardcoding values. This ensures configuration is centralized, version-controlled, and easily maintainable across different environments and deployment scenarios.