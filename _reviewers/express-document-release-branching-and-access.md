---
title: Document release branching and access
description: Release processes must be explicitly documented so that branching strategy
  and publishing permissions are unambiguous for every supported version. Define,
  for each major version being maintained, which branch acts as the "current" branch
  for patch releases (e.g. `master` for the latest major version, `<major>.x` for
  older ones) and which temporary proposal...
repository: expressjs/Express
label: CI/CD
language: Markdown
comments_count: 3
repository_stars: 69579
---

Release processes must be explicitly documented so that branching strategy and publishing permissions are unambiguous for every supported version. Define, for each major version being maintained, which branch acts as the "current" branch for patch releases (e.g. `master` for the latest major version, `<major>.x` for older ones) and which temporary proposal branches are used for minor/major releases (e.g. `<major>.<minor>`), including how pull requests target these branches. Avoid hard-coding `master` in process docs when the real rule is "the active branch for the version being released" — state the rule in version-agnostic terms so it remains correct as new major versions are added.

Similarly, document release permissions using the platform's native access-control mechanisms rather than inventing custom workarounds: GitHub release/tagging rights should map to repository Write/Admin membership, and npm publish rights should be managed via `npm owner add <pkg> <username>` (or the npm org equivalent, once scoped-package support allows it) instead of shared credentials. Keeping both the branch strategy and the access model explicit and centrally documented ensures release automation and manual steps stay consistent across contributors and over time.