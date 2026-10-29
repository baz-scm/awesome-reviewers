---
title: Pin and automate action dependencies
description: 'All third-party GitHub Actions must be pinned to an immutable commit
  SHA (with the version as a trailing comment) rather than a mutable tag, since tags
  can be rewritten and immutable pins are required for supply-chain security (e.g.,
  OSSF Scorecard). Example:'
repository: expressjs/Express
label: CI/CD
language: Yaml
comments_count: 7
repository_stars: 69579
---

All third-party GitHub Actions must be pinned to an immutable commit SHA (with the version as a trailing comment) rather than a mutable tag, since tags can be rewritten and immutable pins are required for supply-chain security (e.g., OSSF Scorecard). Example:

```yaml
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

Once an action is pinned by SHA, configure Dependabot (`.github/dependabot.yml`) to manage version bumps automatically rather than manually re-pinning hashes that are already correct — this avoids wasted effort and keeps updates auditable through PRs. For npm or other ecosystem dependencies managed by Dependabot, scope update rules sensibly (e.g., ignore major version bumps if they are likely to break compatibility, and limit scope to security-relevant updates) so automated PRs stay actionable.

Additionally, prefer minimizing external action dependencies where a simple native alternative exists (e.g., a `curl` call or the built-in `$GITHUB_OUTPUT` mechanism instead of a third-party action) — this reduces both the number of third-party dependencies to vet/pin and the long-term maintenance burden. When adding or reviewing workflow files, always check that third-party actions are SHA-pinned, that Dependabot is configured to track those actions, and that unnecessary action dependencies are replaced with native shell/workflow features when feasible.