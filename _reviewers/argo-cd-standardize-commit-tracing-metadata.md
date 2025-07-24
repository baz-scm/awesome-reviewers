---
title: standardize commit tracing metadata
description: When CI/CD pipelines make automated commits (such as image bumps or manifest
  updates), use standardized git commit trailers to maintain traceability back to
  the original code changes. This enables developers and tools to trace deployment
  artifacts to their source commits.
repository: argoproj/argo-cd
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 20149
---

When CI/CD pipelines make automated commits (such as image bumps or manifest updates), use standardized git commit trailers to maintain traceability back to the original code changes. This enables developers and tools to trace deployment artifacts to their source commits.

Use consistent trailer naming conventions in your CI scripts. Include essential metadata like author, SHA, message, repository URL, and date in ISO 8601 format:

```shell
git commit -m "Bump image to v1.2.3" \
  --trailer "Argocd-related-commit-author: Author Name <author-email>" \
  --trailer "Argocd-related-commit-sha: <code-commit-sha>" \
  --trailer "Argocd-related-commit-message: Commit message of the code commit" \
  --trailer "Argocd-related-commit-repourl: https://git.example.com/owner/repo" \
  --trailer "Argocd-related-commit-date: 2025-06-09T13:50:18-04:00"
```

This approach is particularly important for deployment pipelines where automated tooling pushes changes to DRY manifests after code changes, ensuring full audit trails and enabling effective debugging of deployment issues.