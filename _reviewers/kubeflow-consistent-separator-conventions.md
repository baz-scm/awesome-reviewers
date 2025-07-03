---
title: Consistent separator conventions
description: 'Use appropriate separators in compound identifiers to improve readability
  and ensure naming consistency across the codebase. Specifically:


  1. Use hyphens to separate words in multi-word paths, repository names, and other
  resources:'
repository: kubeflow/kubeflow
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 15064
---

Use appropriate separators in compound identifiers to improve readability and ensure naming consistency across the codebase. Specifically:

1. Use hyphens to separate words in multi-word paths, repository names, and other resources:
   - Correct: `wg-deployment`, `feature-name`
   - Incorrect: `wgdeployment`, `featurename`

2. For version references, use the "vX.Y" format consistently:
   - Correct: `v1.0`, `v2.3`
   - Avoid: `0.Y`, `1.0` (without v prefix)

This practice makes identifiers more readable, maintains consistency with standard conventions, and helps ensure references remain valid over time as the codebase evolves. Consistent naming patterns reduce the need for future refactoring and make documentation more predictable and easier to navigate.
