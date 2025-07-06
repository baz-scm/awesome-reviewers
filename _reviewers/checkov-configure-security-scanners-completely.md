---
title: Configure security scanners completely
description: 'Security scanning tools must be fully configured to maximize detection
  capabilities. When implementing tools like Checkov in CI/CD pipelines:


  1. For Docker-based scanners, use the `--tty` flag for better output handling:'
repository: bridgecrewio/checkov
label: Security
language: Yaml
comments_count: 2
repository_stars: 7668
---

Security scanning tools must be fully configured to maximize detection capabilities. When implementing tools like Checkov in CI/CD pipelines:

1. For Docker-based scanners, use the `--tty` flag for better output handling:
```yaml
-   id: checkov_container
    name: Checkov
    description: This hook runs checkov.
    entry: bridgecrew/checkov:latest -d . --tty
```

2. Enable comprehensive file scanning to detect all potential security issues:
```yaml
-   id: checkov_secrets
    name: Checkov Secrets
    description: This hook looks for secrets with checkov.
    entry: checkov -d . --framework secrets --enable-secret-scan-all-files
```

Improper configuration of security scanners can lead to false negatives, allowing vulnerabilities like leaked secrets, insecure infrastructure configurations, or compliance violations to go undetected. Always verify that security scanning tools are configured with appropriate flags to ensure complete coverage of your codebase.