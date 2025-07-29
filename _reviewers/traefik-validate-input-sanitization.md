---
title: validate input sanitization
description: Always maintain input sanitization and validation mechanisms to prevent
  security vulnerabilities. Disabling built-in security features like path sanitization
  can expose applications to path traversal attacks and routing manipulation.
repository: traefik/traefik
label: Security
language: Markdown
comments_count: 4
repository_stars: 55772
---

Always maintain input sanitization and validation mechanisms to prevent security vulnerabilities. Disabling built-in security features like path sanitization can expose applications to path traversal attacks and routing manipulation.

When working with path sanitization options, avoid disabling security features unless absolutely necessary. If legacy client compatibility requires disabling sanitization, ensure all incoming requests are properly URL-encoded at the application boundary instead.

Example of secure configuration:
```yaml
# Secure - keep sanitization enabled (default)
entryPoints:
  web:
    address: ":80"
    http:
      sanitizePath: true  # Default, recommended

# Insecure - avoid this configuration
entryPoints:
  web:
    address: ":80" 
    http:
      sanitizePath: false  # Creates security vulnerabilities
```

Setting `sanitizePath` to `false` is not safe as it can lead to path interpretation differences between routing rules and backend servers. This can result in unsafe routing when paths contain characters like `/` that aren't properly URL-encoded. Always ensure requests are properly URL-encoded rather than disabling security mechanisms.