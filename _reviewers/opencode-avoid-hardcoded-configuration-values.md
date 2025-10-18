---
title: avoid hardcoded configuration values
description: Configuration values such as URLs, endpoints, timeouts, and environment-specific
  settings should never be hardcoded in source code. Instead, they should be read
  from configuration files, environment variables, or other configurable sources to
  ensure flexibility across different environments and deployments.
repository: sst/opencode
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 28213
---

Configuration values such as URLs, endpoints, timeouts, and environment-specific settings should never be hardcoded in source code. Instead, they should be read from configuration files, environment variables, or other configurable sources to ensure flexibility across different environments and deployments.

Hardcoded values make applications inflexible and difficult to deploy across different environments. They also make it impossible for users to customize behavior according to their specific needs.

Example of what to avoid:
```typescript
// Bad: hardcoded URL
const response = await fetch("http://localhost:11434/api/tags")

// Good: configurable URL
const baseUrl = config.ollama?.baseUrl || "http://localhost:11434"
const response = await fetch(`${baseUrl}/api/tags`)
```

When implementing configuration options, ensure they behave consistently across all applicable contexts. For instance, if a timeout setting is provided, it should apply regardless of the provider type, unless there are specific technical constraints that prevent this.