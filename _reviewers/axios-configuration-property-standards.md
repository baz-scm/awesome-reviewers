---
title: "Configuration property standards"
description: "Always define configuration properties with sensible defaults and consistent naming conventions. When adding new configurable features, establish clear defaults that follow platform conventions and document their purpose."
repository: "axios/axios"
label: "Configurations"
language: "JavaScript"
comments_count: 3
repository_stars: 107000
---

Always define configuration properties with sensible defaults and consistent naming conventions. When adding new configurable features, establish clear defaults that follow platform conventions and document their purpose.

Guidelines:
- Group related configuration properties together in a structured object
- Use descriptive names that clearly indicate the property's purpose
- Provide sensible defaults that work in most common scenarios
- Document the expected values and behavior of each configuration option

Example:
```javascript
const defaults = {
  // HTTP request defaults
  headers: {
    common: {
      'Accept': 'application/json, text/plain, */*'
    }
  },
  
  // Fetch-related configurations
  fetcher: null,
  fetchOptions: {
    cache: 'default',
    redirect: 'follow'
  },
  
  // Character encoding settings
  charset: 'utf-8',
  
  // Feature flags
  experimental_http2: false
};
```

For experimental features, use clearly named boolean flags (like `experimental_http2`). For encoding or format settings, follow platform conventions and provide fallbacks where appropriate (e.g., `config.charset || 'utf-8'`). This approach ensures configurations are discoverable, maintainable, and properly understood by all developers.