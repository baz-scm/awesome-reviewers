---
title: Descriptive consistent naming
description: Use descriptive and consistent names throughout the codebase. Prefer
  full, meaningful names over acronyms or abbreviations to improve readability and
  understanding, especially for newcomers. Maintain naming consistency across different
  files, configurations, and references to the same entity.
repository: kubeflow/kubeflow
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 15064
---

Use descriptive and consistent names throughout the codebase. Prefer full, meaningful names over acronyms or abbreviations to improve readability and understanding, especially for newcomers. Maintain naming consistency across different files, configurations, and references to the same entity.

Examples:
- Prefer `centraldashboard-angular` over `centraldashboard` when referring to the Angular version of the central dashboard
- Use `Access Management` instead of `KFAM` to clearly indicate the component's purpose

When introducing new components or refactoring existing ones, ensure the same naming pattern is followed in all references to maintain consistency and avoid confusion. This includes Makefiles, configuration files, documentation, and code comments.
