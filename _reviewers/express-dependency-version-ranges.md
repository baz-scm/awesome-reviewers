---
title: Dependency version ranges
description: When updating dependencies in package.json, apply a consistent, deliberate
  versioning policy rather than ad-hoc choices. For packages that reliably follow
  semver, prefer caret (^) ranges so consumers automatically receive compatible bug
  fixes and minor updates without manual intervention; reserve exact pins or tilde
  (~) ranges for cases where a wider range...
repository: expressjs/Express
label: Configurations
language: Json
comments_count: 12
repository_stars: 69579
---

When updating dependencies in package.json, apply a consistent, deliberate versioning policy rather than ad-hoc choices. For packages that reliably follow semver, prefer caret (^) ranges so consumers automatically receive compatible bug fixes and minor updates without manual intervention; reserve exact pins or tilde (~) ranges for cases where a wider range is known to be unsafe (e.g., a dependency that previously broke semver, or where a patch bump could cause an unwanted downgrade/upgrade for existing installs). Any change to a dependency's range should be made in its own commit/PR so it can be reviewed and merged independently of unrelated changes.

Before bumping a version, verify:
- It won't silently raise the minimum required Node/npm engine version in a way that breaks existing consumers (check the dependency's own `engines` field and avoid producing confusing install warnings or failures for users with strict engines).
- It won't introduce duplicate copies of the same sub-dependency in the install tree; check the dependency graph and "bubble up" updates to transitive dependencies so the tree stays small.
- The `engines` field in package.json itself uses broad, simple ranges (e.g., `>=8`) rather than overly specific OR-chains tied to LTS cut points, unless there's a concrete compatibility reason.

Example of a safe, well-reasoned update:
```diff
- "cookie-signature": "1.0.6",
+ "cookie-signature": "^1.2.1",
```
vs. a risky one needing a tilde to avoid downgrades:
```diff
- "proxy-addr": "~2.0.5",
+ "proxy-addr": "~2.0.6",
```

Document the agreed-upon policy (caret vs tilde vs pinned) in the project's contribution guidelines so all dependency bumps are handled uniformly, and raise any exceptions (enterprise/legacy npm support, known semver violations) explicitly in the PR description.