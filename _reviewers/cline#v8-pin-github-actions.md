---
title: Pin GitHub Actions
description: 'Third-party GitHub Actions must be pinned to immutable commit SHAs (not
  floating tags like `@v4` or `@v1`) to reduce supply-chain risk.


  Apply this consistently to every workflow step that uses an external action (e.g.,
  both stable and nightly publishing steps). Resolve the tag to the corresponding
  full commit SHA and use that SHA in `uses:`.'
repository: cline/cline#v8
label: Security
language: Yaml
comments_count: 1
repository_stars: 70867
---

Third-party GitHub Actions must be pinned to immutable commit SHAs (not floating tags like `@v4` or `@v1`) to reduce supply-chain risk.

Apply this consistently to every workflow step that uses an external action (e.g., both stable and nightly publishing steps). Resolve the tag to the corresponding full commit SHA and use that SHA in `uses:`.

Example (pattern):
```yaml
- name: Download runtime artifacts
  uses: actions/download-artifact@<FULL_COMMIT_SHA_FOR_v4>
  with:
    path: dist/desktop
    merge-multiple: true

- name: Publish nightly runtime assets
  uses: softprops/action-gh-release@<FULL_COMMIT_SHA_FOR_v1>
```

If you change the tag version, re-resolve and repin to the new commit SHA.