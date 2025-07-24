---
title: minimize credential access scope
description: Apply the principle of least privilege when managing credentials in CI/CD
  pipelines and application code. Use credentials that are limited to only the specific
  permissions required for the task, and remove credentials entirely when they're
  not needed. This reduces security risk by limiting potential access if credentials
  are compromised and makes credential...
repository: docker/compose
label: Security
language: Other
comments_count: 1
repository_stars: 35858
---

Apply the principle of least privilege when managing credentials in CI/CD pipelines and application code. Use credentials that are limited to only the specific permissions required for the task, and remove credentials entirely when they're not needed. This reduces security risk by limiting potential access if credentials are compromised and makes credential rotation easier.

For example, instead of using broad credentials that provide access to multiple services:
```groovy
// Avoid: Using broad credentials with unnecessary permissions
withCredentials([
    usernamePassword(credentialsId: 'orcaeng-hub.docker.com', 
                    usernameVariable: 'REGISTRY_USERNAME', 
                    passwordVariable: 'REGISTRY_PASSWORD')
])
```

Consider creating task-specific credentials or removing them entirely when accessing public resources:
```groovy
// Better: Remove credentials when accessing public resources
// No credentials needed since fossa-analyzer is public on hub
```

Always evaluate whether credentials are actually necessary and ensure they grant only the minimum permissions required for the specific operation.