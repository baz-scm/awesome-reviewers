---
title: externalize configuration values
description: Configuration values, especially sensitive data like API keys and environment-specific
  settings, should be externalized to environment variables rather than hardcoded
  in source code. This prevents sensitive information from being permanently stored
  in git history and enables proper configuration management across different environments.
repository: menloresearch/jan
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 37620
---

Configuration values, especially sensitive data like API keys and environment-specific settings, should be externalized to environment variables rather than hardcoded in source code. This prevents sensitive information from being permanently stored in git history and enables proper configuration management across different environments.

Hardcoded values create security risks and operational inflexibility. When values are committed to version control, they become part of the permanent history and may require credential rotation if exposed.

Example of the problem:
```javascript
// Bad - hardcoded sensitive values
algolia: {
  appId: "Y8QU1SIVLP",
  apiKey: "484787878bcf6f4a26834105f0855fa3",
},
googleTagManager: {
  containerId: "GTM-59R6474K",
}
```

Better approach:
```javascript
// Good - use environment variables
algolia: {
  appId: process.env.ALGOLIA_APP_ID || "default_value",
  apiKey: process.env.ALGOLIA_API_KEY || "default_value",
},
googleTagManager: {
  containerId: process.env.GTM_CONTAINER_ID,
}
```

This approach requires setting up proper environment variable management and updating deployment configurations, but provides better security and flexibility for different environments.