---
title: Complete configuration examples
description: Configuration examples in documentation must be complete and reference
  authoritative sources to prevent deployment issues and developer confusion. Incomplete
  configuration lists can lead to runtime errors and failed setups.
repository: argoproj/argo-cd
label: Configurations
language: Markdown
comments_count: 6
repository_stars: 20149
---

Configuration examples in documentation must be complete and reference authoritative sources to prevent deployment issues and developer confusion. Incomplete configuration lists can lead to runtime errors and failed setups.

When documenting configuration:

1. **Include all required variables**: Don't provide partial lists that may mislead users into thinking the example is complete
2. **Reference authoritative sources**: Point users to definitive configuration sources like Procfile, official schemas, or complete working examples
3. **Add completeness indicators**: Use ellipsis (...) or explicit notes when showing partial configurations

Example of good practice:
```bash
# Example api-server.env file (partial - see Procfile for complete list)
ARGOCD_BINARY_NAME=argocd-server
ARGOCD_FAKE_IN_CLUSTER=true
KUBECONFIG=/Users/<YOUR_USERNAME>/.kube/config # Must be absolute path
...
# For complete environment variables, refer to the Procfile:
# https://github.com/argoproj/argo-cd/blob/master/Procfile
```

Always include notes about:
- Where to find complete configuration references
- Environment-specific requirements (development vs production)
- Path requirements (absolute vs relative)
- Platform-specific variations (Gmail vs generic SMTP)

This prevents users from encountering "incomplete list of env variables" errors and ensures reliable configuration setup across different environments.