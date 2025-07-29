---
title: ensure documentation completeness
description: Documentation should include all necessary information for users to successfully
  implement features. This includes providing complete configuration examples in all
  supported formats, documenting all available options, including prerequisites and
  setup requirements, and adding proper metadata.
repository: traefik/traefik
label: Documentation
language: Markdown
comments_count: 8
repository_stars: 55772
---

Documentation should include all necessary information for users to successfully implement features. This includes providing complete configuration examples in all supported formats, documenting all available options, including prerequisites and setup requirements, and adding proper metadata.

Key completeness requirements:
- **Configuration formats**: Include examples for all applicable formats (YAML, TOML, CLI, Labels, Tags)
- **All options**: Document every configuration parameter, including optional ones with correct default values
- **Prerequisites**: Clearly state setup requirements (e.g., "Before creating IngressRoute objects, you need to apply the Traefik Kubernetes CRDs")
- **Metadata**: Include title and description meta tags for all documentation pages
- **Complete examples**: Show full working examples, not just partial configurations

Example of complete configuration documentation:
```yaml
# Configuration Options
| Field | Description | Default | Required |
|:------|:------------|:--------|:---------|
| `endpoint` | Server endpoint URL | "127.0.0.1:6379" | Yes |
| `headers` | Custom headers to send | {} | No |

# Examples
```yaml tab="File (YAML)"
providers:
  http:
    endpoint: "http://127.0.0.1:9000/api"
    headers:
      Authorization: "Bearer token"
```

```toml tab="File (TOML)"
[providers.http]
  endpoint = "http://127.0.0.1:9000/api"
  [providers.http.headers]
    Authorization = "Bearer token"
```

```bash tab="CLI"
--providers.http.endpoint=http://127.0.0.1:9000/api
--providers.http.headers.Authorization="Bearer token"
```

Incomplete documentation forces users to search elsewhere or make assumptions, leading to implementation errors and poor user experience.