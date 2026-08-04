---
title: Enforce Boundary Least-Privilege
description: Security-sensitive controls must be enforced at the boundary (before
  business logic) and granted with the minimum required scope. Avoid designs where
  access is only checked after the request reaches handlers or where automation receives
  broad credentials.
repository: awslabs/agentcore-samples
label: Security
language: Yaml
comments_count: 2
repository_stars: 3244
---

Security-sensitive controls must be enforced at the boundary (before business logic) and granted with the minimum required scope. Avoid designs where access is only checked after the request reaches handlers or where automation receives broad credentials.

Apply this as follows:
- API/Admin authorization
  - If using Cognito for authentication, also enforce *authorization* (e.g., admin group membership) in a gateway/front-door authorizer so unauthorized callers are rejected before any Lambda handler runs.
  - Do not replicate group checks inside multiple handlers unless the gateway approach is impossible; it’s easy to miss a route and it still allows business logic to execute.

  Example (pattern):
  - Keep your existing Cognito authorizer.
  - Add a second (custom) authorizer that denies invoke unless `cognito:groups` contains the admin group.

  Pseudocode for the custom authorizer decision:
  ```js
  // In custom Lambda authorizer
  const groups = event.requestContext.authorizer.claims['cognito:groups'] || [];
  const isAdmin = Array.isArray(groups) ? groups.includes('admin') : false;
  if (!isAdmin) {
    return generatePolicy('Deny', event.methodArn);
  }
  return generatePolicy('Allow', event.methodArn);
  ```

- Automation/CI permissions
  - Scope GitHub Actions `permissions` to least privilege at the workflow level, then override per-job. Grant `id-token: write` only to jobs that need OIDC role assumption; other jobs should use only `contents: read` or similarly minimal scopes.

  Example:
  ```yaml
  permissions: read-all
  jobs:
    unit:
      permissions:
        contents: read
    e2e:
      permissions:
        contents: read
        id-token: write
  ```

Outcome: fewer authorization gaps across routes and fewer accidental credential overexposures in CI, improving overall security posture.