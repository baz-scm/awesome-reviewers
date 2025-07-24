---
title: explicit security controls
description: Security configurations should use explicit controls and secure defaults
  rather than implicit permissions or hardcoded credentials. This principle helps
  prevent accidental privilege escalation and credential exposure.
repository: argoproj/argo-cd
label: Security
language: Markdown
comments_count: 4
repository_stars: 20149
---

Security configurations should use explicit controls and secure defaults rather than implicit permissions or hardcoded credentials. This principle helps prevent accidental privilege escalation and credential exposure.

Key practices:
- Use secure defaults that require explicit permission grants rather than implicit access
- Avoid hardcoding sensitive values like secrets, keys, or credentials directly in configuration files
- Require explicit RBAC permissions for security-sensitive operations instead of bundling them with broader permissions
- Implement explicit verification policies for deployment artifacts

Example of explicit RBAC configuration:
```yaml
# Explicit logs permission instead of implicit access via applications.get
p, dev-team, logs, get, my-app/*, allow
p, dev-team, applications, get, my-app/*, allow

# Explicit override permission with secure default (disabled)
application.sync.externalRevisionConsideredOverride: 'true'
p, dev-team, applications, override, my-app/*, allow
```

Example of avoiding hardcoded secrets:
```yaml
# Instead of hardcoding in manifests:
# oidc.clientSecret: "hardcoded-secret-value"

# Use kubectl or external secret management:
kubectl create secret generic argocd-secret \
  --from-literal=oidc.clientSecret="your-secret-value"
```

This approach reduces security risks by making security boundaries explicit and preventing accidental exposure of sensitive information.