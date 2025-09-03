---
title: Pin GitHub Actions SHA
description: GitHub Actions should be pinned to specific SHA commits rather than mutable
  tag references to ensure security and reproducibility. Tags can be moved or updated
  by malicious actors, potentially introducing supply chain vulnerabilities, while
  SHA commits are immutable and provide guaranteed consistency across builds.
repository: angular/angular
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 98611
---

GitHub Actions should be pinned to specific SHA commits rather than mutable tag references to ensure security and reproducibility. Tags can be moved or updated by malicious actors, potentially introducing supply chain vulnerabilities, while SHA commits are immutable and provide guaranteed consistency across builds.

When referencing GitHub Actions, always use the full SHA commit hash followed by a comment indicating the version for readability:

```yaml
# Instead of:
uses: cypress-io/github-action@v6

# Use:
uses: cypress-io/github-action@6c143abc292aa835d827652c2ea025d098311070 # v6.10.1
```

This practice protects against supply chain attacks, ensures reproducible builds, and maintains clear version tracking while providing the security benefits of immutable references.