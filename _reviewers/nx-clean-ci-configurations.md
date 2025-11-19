---
title: Clean CI configurations
description: Maintain clean and well-documented CI configurations by removing dead
  code and properly documenting temporary changes. Avoid leaving commented-out code
  in CI files - either remove unused configurations entirely or add proper TODO comments
  with context when temporarily disabling features.
repository: nrwl/nx
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 27518
---

Maintain clean and well-documented CI configurations by removing dead code and properly documenting temporary changes. Avoid leaving commented-out code in CI files - either remove unused configurations entirely or add proper TODO comments with context when temporarily disabling features.

When removing unused configurations, delete them completely rather than commenting them out. For temporary disabling due to issues, add TODO comments with explanations and follow-up plans.

Example:
```yaml
# Good - Clean removal
node_version:
  - 20
  - 22
  - 24

# Good - Temporary disable with context  
# TODO(v23): remove node 20 - EOL April 2026
# TODO: Re-enable Windows builds after fixing Gradle issue (assigned to @xiongemi)
# - os: windows-latest
#   node_version: 22

# Bad - Unexplained commented code
# - 23
```

This practice keeps CI configurations maintainable, reduces confusion for team members, and ensures temporary changes don't become permanent oversights.