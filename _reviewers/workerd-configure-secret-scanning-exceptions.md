---
title: Configure secret scanning exceptions
description: When embedding test certificates or cryptographic keys in code for testing
  purposes, configure secret scanning tools to exclude these legitimate test artifacts
  to prevent false positive alerts. This ensures security tooling remains effective
  while avoiding alert fatigue that could lead to ignoring genuine security issues.
repository: cloudflare/workerd
label: Security
language: JavaScript
comments_count: 1
repository_stars: 6989
---

When embedding test certificates or cryptographic keys in code for testing purposes, configure secret scanning tools to exclude these legitimate test artifacts to prevent false positive alerts. This ensures security tooling remains effective while avoiding alert fatigue that could lead to ignoring genuine security issues.

Test certificates and keys should be added to your repository's secret scanning configuration file (e.g., `.github/secret_scanning.yml`) to explicitly mark them as safe. This practice maintains the integrity of automated security scanning while allowing necessary test infrastructure.

Example configuration:
```yaml
# .github/secret_scanning.yml
paths-ignore:
  - "src/workerd/api/tests/starttls-try-server.js"
```

This approach balances security automation with development needs, ensuring that security tools continue to catch real secrets while not flagging intentional test data.