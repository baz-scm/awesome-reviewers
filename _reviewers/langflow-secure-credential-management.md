---
title: Secure credential management
description: Ensure sensitive data like API keys, passwords, and encryption keys are
  stored securely and never exposed in code, configuration files, or documentation.
  This prevents credential leakage and unauthorized access to external services and
  systems.
repository: langflow-ai/langflow
label: Security
language: Other
comments_count: 3
repository_stars: 111046
---

Ensure sensitive data like API keys, passwords, and encryption keys are stored securely and never exposed in code, configuration files, or documentation. This prevents credential leakage and unauthorized access to external services and systems.

**Key practices:**
- Store sensitive data in secure external systems (Kubernetes secrets, external secret managers, environment variables)
- Avoid embedding secrets directly in configuration files, flow JSON files, or code
- Use proper encryption for sensitive data at rest and in transit
- Truncate or omit actual credential values in documentation and examples

**Example secure configuration:**
```yaml
# Good: Reference secrets from secure storage
env:
  - name: OPENAI_API_KEY
    valueFrom:
      secretKeyRef:
        name: api-secrets
        key: openai-key
  - name: LANGFLOW_SECRET_KEY
    valueFrom:
      secretKeyRef:
        name: langflow-secrets
        key: secret-key
```

**Example documentation:**
```text
# Good: Truncated example
LANGFLOW_SECRET_KEY=dBuu...2kM2_fb

# Bad: Full credential exposed
LANGFLOW_SECRET_KEY=dBuuuB_FHLvU8T9eUNlxQF9ppqRxwWpXXQ42kM2_fb
```

This practice is especially critical in production environments where credential exposure can lead to data breaches, unauthorized system access, and compromise of connected services.