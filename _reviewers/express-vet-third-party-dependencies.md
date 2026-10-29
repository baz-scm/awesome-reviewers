---
title: Vet third-party dependencies
description: Before adding any new dependency, verify it is legitimate, actively maintained,
  and actually necessary—never add a package that merely duplicates or shadows built-in
  functionality (e.g., the npm 'path' package, which is just a copy of Node's core
  'path' module). Unvetted or redundant dependencies expand the supply-chain attack
  surface and can introduce...
repository: Expressjs/Express
label: Security
language: Json
comments_count: 1
repository_stars: 69580
---

Before adding any new dependency, verify it is legitimate, actively maintained, and actually necessary—never add a package that merely duplicates or shadows built-in functionality (e.g., the npm 'path' package, which is just a copy of Node's core 'path' module). Unvetted or redundant dependencies expand the supply-chain attack surface and can introduce malicious or unmaintained code. When a built-in module already provides the required functionality, use it directly instead of pulling in an external package. As part of code review, check package.json diffs for new dependencies and confirm their source, popularity, and purpose before merging.