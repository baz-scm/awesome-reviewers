---
title: Justify dependency changes
description: Always provide clear justification when modifying dependency configurations,
  including version updates, dependency types, or new additions. Consider the impact
  on stability, compatibility, and end users before making changes.
repository: microsoft/playwright
label: Configurations
language: Json
comments_count: 2
repository_stars: 76113
---

Always provide clear justification when modifying dependency configurations, including version updates, dependency types, or new additions. Consider the impact on stability, compatibility, and end users before making changes.

For version updates, avoid unnecessary churn by sticking with working versions unless there's a compelling reason to upgrade (security fixes, required features, bug fixes). For dependency types, choose between regular dependencies, devDependencies, and peerDependencies based on actual usage patterns and user compatibility needs.

Example considerations:
- Version updates: "Can we stick with the old version we already had to avoid unnecessary deps churn?"
- Dependency types: When adding peerDependencies, consider if users need flexibility with major versions vs. the complexity it introduces
- Compatibility: "If we hard-depend on Angular 18, we can cause problems to users who didn't migrate to Angular 18 yet"

Document the reasoning behind dependency configuration decisions to help future maintainers understand the trade-offs made.