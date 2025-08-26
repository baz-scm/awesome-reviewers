---
title: automate frequent releases
description: Implement automated release workflows to publish updates frequently and
  consistently across all distribution channels. Manual release processes create bottlenecks
  that force consumers to pin dependencies to specific commit SHAs instead of using
  stable releases.
repository: tree-sitter/tree-sitter
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 21799
---

Implement automated release workflows to publish updates frequently and consistently across all distribution channels. Manual release processes create bottlenecks that force consumers to pin dependencies to specific commit SHAs instead of using stable releases.

Set up CI/CD pipelines that automatically publish to all relevant package managers (crates.io, NPM, GitHub releases) after each merged PR or batch of changes. This reduces maintenance overhead and ensures consumers can rely on regular releases rather than tracking development commits.

Example automation approach:
```yaml
# .github/workflows/release.yml
on:
  push:
    branches: [main]
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Publish to crates.io
        run: cargo publish
      - name: Publish Node.js bindings to NPM
        run: npm publish
      - name: Create GitHub release with artifacts
        run: gh release create v${{ env.VERSION }}
```

Frequent automated releases eliminate the need for consumers to pin to commit SHAs and ensure that fixes and improvements reach users promptly without requiring manual intervention from maintainers.