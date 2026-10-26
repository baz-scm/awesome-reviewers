---
title: Pin GitHub Actions
description: Third-party GitHub Actions should be pinned to immutable commit SHAs
  instead of floating version tags (e.g., `@v4`, `@v1`) to reduce supply-chain risk.
  Apply this consistently across all workflow steps (including stable and nightly
  release/publish jobs).
repository: cline/cline#v16
label: Security
language: Yaml
comments_count: 1
repository_stars: 70882
---

Third-party GitHub Actions should be pinned to immutable commit SHAs instead of floating version tags (e.g., `@v4`, `@v1`) to reduce supply-chain risk. Apply this consistently across all workflow steps (including stable and nightly release/publish jobs).

Example:
```yaml
- name: Download runtime artifacts
  uses: actions/download-artifact@<FULL_COMMIT_SHA>
  with:
    path: dist/desktop
    merge-multiple: true

- name: Publish nightly runtime assets
  uses: softprops/action-gh-release@<FULL_COMMIT_SHA>
```

Rule of thumb: if a `uses:` reference contains only a major/minor tag (like `@v4`), update it to the full commit SHA you intend to trust and maintain.