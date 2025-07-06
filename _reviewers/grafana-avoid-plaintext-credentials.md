---
title: Avoid plaintext credentials
description: Never include plaintext passwords or credentials in connection strings,
  configuration files, or documentation examples. This creates security vulnerabilities
  as credentials could be exposed in logs, version control, or to unauthorized personnel.
repository: grafana/grafana
label: Security
language: Markdown
comments_count: 1
repository_stars: 68825
---

Never include plaintext passwords or credentials in connection strings, configuration files, or documentation examples. This creates security vulnerabilities as credentials could be exposed in logs, version control, or to unauthorized personnel.

Instead:
- Use environment variables for sensitive information
- Leverage secure credential storage systems like secret managers
- Implement connection pooling with secure authentication
- Use password files with appropriate permissions

Example - Replace this insecure approach:
```
postgresql://user:password@host:5432/dbname
```

With a more secure alternative:
```
postgresql://${DB_USER}:${DB_PASSWORD}@host:5432/dbname
```

Where environment variables or a secrets manager handles the actual credentials. When providing documentation or examples, always include warnings about security implications of different connection methods.