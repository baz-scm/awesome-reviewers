---
title: Follow established naming patterns
description: When introducing new identifiers (variables, methods, flags, metrics,
  etc.), examine existing code to identify and follow established naming conventions
  rather than creating new patterns. This ensures consistency across the codebase
  and maintains predictability for users and developers.
repository: argoproj/argo-cd
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 20149
---

When introducing new identifiers (variables, methods, flags, metrics, etc.), examine existing code to identify and follow established naming conventions rather than creating new patterns. This ensures consistency across the codebase and maintains predictability for users and developers.

Before naming new elements, look for similar existing components and adopt their naming patterns. For example, when adding CLI flags, follow the pattern of sibling commands using long descriptive names like `--app-namespace` and `--hard-refresh`. For metrics, follow established conventions like appending `_total` to counter metrics (e.g., `argocd_login_request_total` instead of `argocd_login_request`).

This approach prevents naming inconsistencies that can confuse users and makes the codebase more maintainable by establishing predictable patterns that developers can easily follow.