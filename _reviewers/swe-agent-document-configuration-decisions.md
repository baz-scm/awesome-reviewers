---
title: Document configuration decisions
description: When making configuration changes, especially those involving version
  specifications or constraints, include explanatory comments with links to relevant
  issues, PRs, or documentation. This provides context for future maintainers and
  makes the reasoning behind configuration decisions transparent and traceable.
repository: SWE-agent/SWE-agent
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 16839
---

When making configuration changes, especially those involving version specifications or constraints, include explanatory comments with links to relevant issues, PRs, or documentation. This provides context for future maintainers and makes the reasoning behind configuration decisions transparent and traceable.

For dependency versions, document why specific version constraints were chosen:
```yaml
dependencies:
  - together>=1.1.0  # Use >= for compatibility, see issue #236
```

For CI/CD matrices, explain version selection rationale:
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12"]  # Dropped 3.10 support, see PR #123
```

This practice helps team members understand the historical context of configuration decisions and prevents unnecessary changes or confusion during future updates.