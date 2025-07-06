---
title: Avoid wildcard permissions
description: Implement the principle of least privilege by avoiding wildcard permissions
  (e.g., '*') in access control policies. Always specify only the exact permissions
  required for a resource or action. When analyzing existing policies with wildcards,
  use tools that expand wildcards into specific permissions to understand the full
  security implications.
repository: bridgecrewio/checkov
label: Security
language: Markdown
comments_count: 1
repository_stars: 7667
---

Implement the principle of least privilege by avoiding wildcard permissions (e.g., '*') in access control policies. Always specify only the exact permissions required for a resource or action. When analyzing existing policies with wildcards, use tools that expand wildcards into specific permissions to understand the full security implications.

For AWS IAM policies, consider using the IAM_ACTION_EXPANSION extension which adds additional data to the `Action` field by expanding wildcards to actual actions, enabling more precise security analysis:

```yaml
metadata:
  id: "CKV2_CUSTOM_1"
  extensions:
    - IAM_ACTION_EXPANSION
```

Example of permission best practices:

```yaml
# Instead of overly permissive policies like:
Action: 
  - s3:*

# Use specific permissions:
Action:
  - s3:GetObject
  - s3:PutObject
```

When security tools analyze your policies, extensions like IAM_ACTION_EXPANSION can help by automatically expanding wildcards for more precise permission analysis and vulnerability detection.