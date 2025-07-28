---
title: Configuration value safety
description: Ensure configuration values are properly encoded and dependencies use
  specific versions to prevent runtime failures and security issues. When embedding
  dynamic values in YAML configuration files, use proper encoding methods like `.to_json`
  to handle special characters safely. For external dependencies in workflows and
  configuration, specify exact versions...
repository: mastodon/mastodon
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 48691
---

Ensure configuration values are properly encoded and dependencies use specific versions to prevent runtime failures and security issues. When embedding dynamic values in YAML configuration files, use proper encoding methods like `.to_json` to handle special characters safely. For external dependencies in workflows and configuration, specify exact versions rather than using `@latest` or similar floating tags.

Example of proper value encoding:
```yaml
# Instead of:
password: <%= ENV.fetch('SMTP_PASSWORD', nil) %>

# Use:
password: <%= ENV.fetch('SMTP_PASSWORD', nil).to_json %>
```

Example of proper version pinning:
```yaml
# Instead of:
uses: chromaui/action@latest

# Use:
uses: chromaui/action@v1
```

This prevents configuration parsing errors when values contain special characters and ensures reproducible builds by avoiding unexpected dependency updates.