---
title: Configuration requirements clarity
description: Configuration requirements and dependencies should be made explicit and
  prominent in documentation, not buried in notes or admonitions. When introducing
  new configuration options or requirements, ensure they are clearly documented as
  prerequisites or explicit steps rather than side notes that users might miss.
repository: gravitational/teleport
label: Configurations
language: Other
comments_count: 5
repository_stars: 19109
---

Configuration requirements and dependencies should be made explicit and prominent in documentation, not buried in notes or admonitions. When introducing new configuration options or requirements, ensure they are clearly documented as prerequisites or explicit steps rather than side notes that users might miss.

Key practices:
- Move critical configuration requirements from admonitions/notes to main documentation flow
- Create explicit configuration steps rather than mentioning requirements in passing
- Provide explanatory context before showing configuration examples
- Make RBAC and access control requirements prominent and actionable

Example of good practice:
```yaml
# Clear prerequisite documentation
## Prerequisites
- Teleport role version 8 requires app_labels configuration
- Ensure your role allows access with proper label matching

## Step X: Configure Access
Configure the required app_labels for RBAC:
```yaml
allow:
  app_labels:
    'teleport.dev/origin': 'aws-identity-center'
```

This approach ensures users understand configuration requirements upfront rather than discovering them through error messages or buried documentation notes.