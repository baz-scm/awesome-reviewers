---
title: Prevent sensitive data exposure
description: Never log or store sensitive information (passwords, tokens, secrets)
  in clear text. This common security vulnerability can lead to credential leaks and
  unauthorized access.
repository: bridgecrewio/checkov
label: Security
language: Python
comments_count: 20
repository_stars: 7667
---

Never log or store sensitive information (passwords, tokens, secrets) in clear text. This common security vulnerability can lead to credential leaks and unauthorized access.

When logging:
1. Remove sensitive data from logs entirely
2. If logging is necessary, hash or mask the sensitive values
3. Use specialized logging frameworks that automatically redact sensitive fields

For example, instead of:
```python
logging.info(f"cloning {git_url} to {clone_dir}")  # git_url may contain credentials
```

Use:
```python
# Extract and mask sensitive parts
safe_url = git_url if '@' not in git_url else git_url.split('@')[1]  
logging.info(f"cloning {safe_url} to {clone_dir}")
```

When handling secrets:
1. Never store secrets in clear text variables
2. Use environment variables or dedicated secret management services
3. Implement proper filtering for references to vault secrets
4. Add validation to prevent accidental logging of secrets

Remember that exposing sensitive data in logs is a common finding in security audits and can lead to significant security breaches. Consistently audit your code for instances of clear-text logging or storage of sensitive information.