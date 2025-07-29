---
title: maintain IAM role isolation
description: Each resource should use the IAM role assigned to its associated function
  rather than sharing roles across different functional boundaries. Sharing roles
  between different functions or resources can create security vulnerabilities and
  potential privilege escalation paths.
repository: serverless/serverless
label: Security
language: JavaScript
comments_count: 1
repository_stars: 46810
---

Each resource should use the IAM role assigned to its associated function rather than sharing roles across different functional boundaries. Sharing roles between different functions or resources can create security vulnerabilities and potential privilege escalation paths.

When configuring resources like scheduled events, always ensure they use the same role as their associated function:

```javascript
// Preferred: Use the function's specific role
const functionLogicalId = this.provider.naming.getLambdaLogicalId(functionName);
const functionResource = resources[functionLogicalId];
roleArn = functionResource.Properties.Role;

// Avoid: Using a shared default role across different functions
roleArn = { 'Fn::GetAtt': ['IamRoleLambdaExecution', 'Arn'] };
```

This approach maintains proper security isolation, prevents unintended cross-function access, and aligns with the principle of least privilege. Many users prefer to have IAM permissions isolated and configured per function to avoid security breaches where one function's resources inadvertently rely on roles dedicated to other functions.