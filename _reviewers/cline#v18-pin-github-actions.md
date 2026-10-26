---
title: Pin GitHub Actions
description: 'Treat GitHub Actions as external dependencies: avoid floating version
  tags in `uses:` and pin every third-party action to an immutable full commit SHA.'
repository: cline/cline#v18
label: Security
language: Yaml
comments_count: 1
repository_stars: 70884
---

Treat GitHub Actions as external dependencies: avoid floating version tags in `uses:` and pin every third-party action to an immutable full commit SHA.

Why: tags like `v1`/`v4` can move over time, enabling unexpected (or malicious) changes via the action supply chain.

How to apply:
- For every `uses: owner/repo@<tag>`, look up the action’s commit SHA for that release tag.
- Replace the tag with the full SHA and do it consistently across all workflow steps (e.g., stable and nightly).

Example:
```yaml
steps:
  - name: Download runtime artifacts
    uses: actions/download-artifact@<FULL_COMMIT_SHA>
    with:
      path: dist/desktop
      merge-multiple: true

  - name: Publish nightly runtime assets
    uses: softprops/action-gh-release@<FULL_COMMIT_SHA>
```