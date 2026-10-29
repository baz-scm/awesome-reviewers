---
title: Dependency version ranges
description: When editing dependency versions in package.json, follow the team's agreed
  semver range convention rather than mixing styles ad hoc. Unless there is a specific
  compatibility reason, prefer caret (`^`) ranges for both dependencies and devDependencies,
  and update version specifiers in their own dedicated commits/PRs rather than bundling
  them with unrelated...
repository: Expressjs/Express
label: Configurations
language: Json
comments_count: 14
repository_stars: 69580
---

When editing dependency versions in package.json, follow the team's agreed semver range convention rather than mixing styles ad hoc. Unless there is a specific compatibility reason, prefer caret (`^`) ranges for both dependencies and devDependencies, and update version specifiers in their own dedicated commits/PRs rather than bundling them with unrelated changes. Before bumping a dependency, verify:
- It does not require a newer Node.js version than declared in the `engines` field (e.g., don't add a package needing Node 10+ if `engines` still allows Node 0.10).
- The bump does not introduce a user-facing breaking change (e.g., a major qs or depd upgrade) unless it is intentionally scoped to a major release.
- It won't create duplicate copies of a sub-dependency in the install tree; if a transitive dependency already pins a version, bump it at the source so the tree stays deduplicated.
- Widening a range (e.g., removing `~` for `^`) won't allow an unintended downgrade or breaking patch for users upgrading from an older minor version.

Example of correct update:
```diff
-    "cookie-signature": "1.0.6",
+    "cookie-signature": "^1.2.1",
```
not:
```diff
-    "cookie-signature": "1.0.6",
+    "cookie-signature": "1.1.0",
```
which silently tightens Node engine requirements and risks breaking installs for users with strict engine checks.