---
title: Pin actions to commit SHA
description: All third-party GitHub Actions referenced in workflows must be pinned
  to a full commit SHA rather than a mutable tag or branch, since tags can be rewritten
  and this breaks the immutability/security guarantees required for supply-chain integrity
  (this is also an OSSF Scorecard requirement). Always include a trailing comment
  with the human-readable version...
repository: Expressjs/Express
label: CI/CD
language: Yaml
comments_count: 6
repository_stars: 69580
---

All third-party GitHub Actions referenced in workflows must be pinned to a full commit SHA rather than a mutable tag or branch, since tags can be rewritten and this breaks the immutability/security guarantees required for supply-chain integrity (this is also an OSSF Scorecard requirement). Always include a trailing comment with the human-readable version for clarity, e.g.:

```yaml
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

Do not manually update a SHA that is already pinned "just because" you're touching the file — once an action is on a commit SHA, let Dependabot handle version bumps so the update goes through its usual security-reviewed PR flow. Make sure a `dependabot.yml` exists with a `github-actions` ecosystem entry (in addition to `npm` or other ecosystems used by the project) so pinned actions are kept current automatically:

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly

  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
```

Exceptions can be made for highly trusted first-party actions (e.g. those published directly by GitHub, Microsoft, or AWS) where floating on a major-version tag may be acceptable, but the default and preferred approach is commit-SHA pinning with Dependabot-driven updates.