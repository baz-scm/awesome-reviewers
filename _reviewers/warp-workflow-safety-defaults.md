---
title: Workflow safety defaults
description: When authoring CI/CD workflows, make configuration choices that (1) match
  the actual capabilities required by downstream steps and (2) use conservative, contributor-safe
  defaults for automated cleanup.
repository: warpdotdev/warp
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 56893
---

When authoring CI/CD workflows, make configuration choices that (1) match the actual capabilities required by downstream steps and (2) use conservative, contributor-safe defaults for automated cleanup.

- If any step needs historical git data (e.g., `git blame`, changelog generation, diffing across tags/commits), ensure the checkout includes sufficient history (commonly full history via `fetch-depth: 0`) and don’t remove it without verifying the dependency.
- For automation that closes/archives issues or other contributor-facing items, prefer longer response windows unless you can justify more aggressive settings (e.g., give ~1–2 weeks rather than only a few days).

Example (git history):
```yaml
- uses: actions/checkout@v4
  with:
    ref: ${{ needs.analyze.outputs.analyzed_sha }}
    fetch-depth: 0  # required for git blame/history-based steps
```

Example (conservative stale closure):
```js
const LABEL = 'needs-info';
const BUSINESS_DAYS = 10; // ~1–2 weeks; adjust only with a strong reason
```