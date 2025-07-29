---
title: verify authorization permissions
description: Ensure that authorization checks use the appropriate permission level
  for the specific operation being performed. Operations that only read data should
  use READ permissions, while operations that modify data should use WRITE permissions.
  Using overly permissive authorization can lead to privilege escalation vulnerabilities.
repository: apache/kafka
label: Security
language: Other
comments_count: 1
repository_stars: 30575
---

Ensure that authorization checks use the appropriate permission level for the specific operation being performed. Operations that only read data should use READ permissions, while operations that modify data should use WRITE permissions. Using overly permissive authorization can lead to privilege escalation vulnerabilities.

For example, when implementing authorization for share group operations:
```scala
// Incorrect - using WRITE for a read operation
if (!authHelper.authorize(request.context, WRITE, GROUP, groupId)) {

// Correct - using READ for a read operation  
if (!authHelper.authorize(request.context, READ, GROUP, groupId)) {
```

Always verify that the permission level matches the actual data access pattern of the operation to maintain proper access control boundaries.