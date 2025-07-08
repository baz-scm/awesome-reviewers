---
title: Least privilege principle
description: 'Always follow the principle of least privilege by granting the minimum
  permissions necessary for functionality. This applies to various security contexts:'
repository: prowler-cloud/prowler
label: Security
language: Python
comments_count: 6
repository_stars: 11834
---

Always follow the principle of least privilege by granting the minimum permissions necessary for functionality. This applies to various security contexts:

1. **OAuth scopes**: Request only the specific permissions needed:
```python
# BAD: Requesting excessive permissions
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "SCOPE": [
            "user",
            "repo", # Grants full access to repositories
        ],
    },
}

# GOOD: Request only what's needed
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "SCOPE": [
            "user", # Only user information
        ],
    },
}
```

2. **Default to secure values**: When uncertain about security settings, default to the more secure option:
```python
# BAD: Defaulting to insecure value
allow_security_end_user_reporting=global_meeting_policy.get(
    "AllowSecurityEndUserReporting", True
)

# GOOD: Default to secure value
allow_security_end_user_reporting=global_meeting_policy.get(
    "AllowSecurityEndUserReporting", False
)
```

3. **Authentication flows**: Implement proper validation with clear error paths that provide minimal information to unauthenticated users.

4. **Access control**: Avoid public access by default for all resources. For AWS services specifically, check and remove any policy statements with wildcard principals:
```python
# Replace public access policies with specific account-based access
trusted_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"AWS": f"arn:{audited_partition}:iam::{account_id}:root"},
        "Action": "sqs:*",
        "Resource": resource_arn
    }]
}
```

Regularly audit permissions and be vigilant about actions that could lead to privilege escalation, such as `iam:PassRole` or other powerful IAM actions.