---
title: Pin Actions to SHAs
description: For GitHub Actions, pin every third-party `uses:` dependency to an immutable
  commit SHA (not a moving tag like `@v1`/`@v4`). Apply this consistently to all workflow
  variants (e.g., stable and nightly) to reduce supply-chain risk from action updates.
repository: cline/cline#v15
label: Security
language: Yaml
comments_count: 1
repository_stars: 70877
---

For GitHub Actions, pin every third-party `uses:` dependency to an immutable commit SHA (not a moving tag like `@v1`/`@v4`). Apply this consistently to all workflow variants (e.g., stable and nightly) to reduce supply-chain risk from action updates.

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
Use the commit SHA returned by the action’s “pin to a commit” guidance (or `@<SHA>` directly) and update it intentionally during scheduled maintenance.