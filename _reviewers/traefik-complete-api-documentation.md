---
title: complete API documentation
description: Ensure all API configuration options are fully documented with accurate
  default values, required field indicators, and complete parameter tables. Missing
  configuration options, incorrect defaults, or incomplete documentation tables create
  confusion and implementation errors for developers.
repository: traefik/traefik
label: API
language: Markdown
comments_count: 5
repository_stars: 55772
---

Ensure all API configuration options are fully documented with accurate default values, required field indicators, and complete parameter tables. Missing configuration options, incorrect defaults, or incomplete documentation tables create confusion and implementation errors for developers.

When documenting API interfaces, configuration providers, or middleware options:

1. **Include all available options** - Don't omit configuration parameters that users can set
2. **Specify accurate defaults** - Use correct default values (e.g., `[]` for arrays, `""` for strings, specific values where applicable)  
3. **Mark required fields correctly** - Clearly indicate which parameters are mandatory vs optional
4. **Provide complete examples** - Include required parameters in code examples, especially when they have no defaults

Example of complete API documentation:

```yaml
# Configuration Options Table
| Field      | Description                                           | Default | Required |
|:-----------|:-----------------------------------------------------|:--------|:---------|
| `endpoint` | HTTP(S) endpoint URL for the provider               | ""      | Yes      |
| `status`   | Status codes that trigger error pages               | []      | No       |
| `preserveRequestMethod` | Preserve original request method during forwarding | false   | No       |
```

This prevents developers from encountering undocumented options, incorrect assumptions about defaults, or missing required configuration that leads to runtime errors.