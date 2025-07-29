---
title: configuration examples accuracy
description: Ensure configuration examples and documentation use current, supported
  syntax and accurately reflect the actual behavior of the system. Avoid promoting
  deprecated features, outdated versions, or configuration options that have no effect.
repository: serverless/serverless
label: Configurations
language: Markdown
comments_count: 6
repository_stars: 46810
---

Ensure configuration examples and documentation use current, supported syntax and accurately reflect the actual behavior of the system. Avoid promoting deprecated features, outdated versions, or configuration options that have no effect.

Key practices:
- Use current runtime versions in examples (e.g., `nodejs18.x`, `python3.9`) instead of outdated ones (`nodejs6.x`, `python2.7`)
- Promote current syntax over deprecated alternatives (e.g., `iam.role.statements` instead of `iamRoleStatements`)
- Remove configuration examples that have no actual effect on the system
- Verify that statements about required vs optional configuration are accurate
- Use proper semantic version constraints that don't inadvertently allow incompatible future versions

Example of good practice:
```yaml
# Good: Uses current syntax and supported versions
provider:
  name: aws
  runtime: nodejs18.x
  iam:
    role:
      statements:
        - Effect: Allow
          Action: 's3:GetObject'
          Resource: '*'

# Bad: Uses deprecated syntax and outdated versions  
provider:
  name: aws
  runtime: nodejs6.x
  iamRoleStatements:
    - Effect: Allow
      Action: 's3:GetObject'
      Resource: '*'
```

This prevents developers from copying ineffective or outdated configuration patterns that may cause deployment issues or use deprecated features.