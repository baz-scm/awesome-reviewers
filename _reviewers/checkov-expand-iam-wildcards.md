---
title: Expand IAM wildcards
description: 'Always expand IAM wildcard permissions (`*`) to specific actions for
  thorough security analysis. Wildcard permissions can unintentionally grant excessive
  access, creating security vulnerabilities. '
repository: bridgecrewio/checkov
label: Security
language: Markdown
comments_count: 1
repository_stars: 7668
---

Always expand IAM wildcard permissions (`*`) to specific actions for thorough security analysis. Wildcard permissions can unintentionally grant excessive access, creating security vulnerabilities. 

Use the IAM_ACTION_EXPANSION extension in your security scanning tools to automatically expand wildcards to specific permissions:

```yaml
metadata:
  id: "CKV2_CUSTOM_1"
  extensions:
    - IAM_ACTION_EXPANSION
```

This allows for precise permission auditing and helps identify overly permissive policies that might violate the principle of least privilege.