---
title: Review security permissions
description: Carefully review all security permissions and privileges to ensure they
  follow the principle of least privilege. Avoid coupling unrelated permissions together
  and verify that elevated privileges are truly necessary.
repository: volcano-sh/volcano
label: Security
language: Yaml
comments_count: 2
repository_stars: 4899
---

Carefully review all security permissions and privileges to ensure they follow the principle of least privilege. Avoid coupling unrelated permissions together and verify that elevated privileges are truly necessary.

When defining RBAC roles, separate concerns appropriately rather than bundling unrelated permissions. For example, avoid coupling PriorityClass permissions with job management permissions when they serve different purposes and can be granted through separate mechanisms.

When granting elevated security capabilities like DAC_OVERRIDE, SETUID, SETGID, or SETFCAP, explicitly verify and document why these privileges are required. Consider the security implications and ensure proper justification.

Example of proper separation:
```yaml
# Good: Focused role for vcjob management only
rules:
  - apiGroups: ["batch.volcano.sh"]
    resources: ["jobs"]
    verbs: ["create", "get", "list", "update", "delete"]
# PriorityClass permissions handled separately through other roles
```

Example of privilege verification:
```yaml
# Document and verify elevated capabilities
securityContext:
  capabilities:
    add: ["DAC_OVERRIDE", "SETUID", "SETGID", "SETFCAP"]
    # Verified: These capabilities are required for [specific functionality]
```