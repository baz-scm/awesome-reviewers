---
title: parameterize configuration values
description: Avoid hardcoded values in configuration files and templates. Make settings
  parameterizable with sensible defaults to accommodate different environments and
  use cases. Even when you're unsure if a setting needs to be configurable, err on
  the side of flexibility - most users will stick with defaults, but those who need
  customization will appreciate the option.
repository: gravitational/teleport
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 19109
---

Avoid hardcoded values in configuration files and templates. Make settings parameterizable with sensible defaults to accommodate different environments and use cases. Even when you're unsure if a setting needs to be configurable, err on the side of flexibility - most users will stick with defaults, but those who need customization will appreciate the option.

Example of problematic hardcoded configuration:
```yaml
# Bad: hardcoded values
proxy_server: lukeo.teleport-test.com:443
discovery_interval: 10m  # fixed, no way to change
```

Example of properly parameterized configuration:
```yaml
# Good: parameterized with defaults
proxy_server: {{ .Values.proxyServer | default "example.teleport-test.com:443" }}
discovery_interval: {{ .Values.discoveryInterval | default "10m" }}
```

This approach ensures configurations work across different environments while maintaining reasonable defaults for common scenarios. As one reviewer noted: "Hard to think of a default that is good for everyone" - parameterization solves this by letting each deployment choose what works best.