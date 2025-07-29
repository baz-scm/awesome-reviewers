---
title: configuration value consistency
description: Ensure configuration values follow consistent formats, use meaningful
  defaults, and accurately distinguish between required and optional fields across
  all documentation.
repository: traefik/traefik
label: Configurations
language: Markdown
comments_count: 18
repository_stars: 55772
---

Ensure configuration values follow consistent formats, use meaningful defaults, and accurately distinguish between required and optional fields across all documentation.

Configuration inconsistencies can lead to user confusion and deployment failures. This standard addresses several critical areas:

**Format Consistency:**
- Time durations should include units: `deadPeriod: 2d` not `deadPeriod: 2`
- Environment variables should use proper syntax: `TRAEFIK_LOG_LEVEL="INFO"` not `TRAEFIK_LOG_LEVEL=INFO`
- CLI arguments should be properly quoted: `--providers.ecs.constraints="Label(\`key\`,\`value\`)"` not `--providers.ecs.constraints=Label(\`key\`,\`value\`)`

**Default Value Accuracy:**
- Avoid "N/A" or meaningless defaults in configuration tables
- Mark options as "Required" only when no meaningful default exists
- Use empty strings `""` for truly optional string fields
- Document when default values are environment-specific (e.g., `127.0.0.1:2379` for local testing only)

**Provider-Specific Differences:**
- Clearly document when Kubernetes CRD providers use different field names (e.g., `secret` instead of `users` for authentication)
- Include provider-specific examples for cross-provider configurations
- Note when certain options don't apply to specific providers

**Example of proper configuration documentation:**
```yaml
| Field | Description | Default | Required |
|-------|-------------|---------|----------|
| `redis.endpoints` | Redis server endpoints | `""` | Yes |
| `redis.db` | Database number | `0` | No |
| `redis.tls.insecureSkipVerify` | Skip TLS verification | `false` | No |
```

This approach prevents configuration errors and provides clear guidance for users across different deployment scenarios.