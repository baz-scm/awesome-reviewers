---
title: Manage testing dependencies
description: Properly manage testing-related dependencies by placing them in devDependencies
  and regularly auditing them to remove redundant tools. Test-only packages should
  never appear in regular dependencies, and outdated testing libraries should be removed
  when newer alternatives are already present in the project.
repository: nestjs/nest
label: Testing
language: Json
comments_count: 2
repository_stars: 71766
---

Properly manage testing-related dependencies by placing them in devDependencies and regularly auditing them to remove redundant tools. Test-only packages should never appear in regular dependencies, and outdated testing libraries should be removed when newer alternatives are already present in the project.

Examples:
- Add testing frameworks like nunjucks in devDependencies:
  ```diff
       "mysql": "2.18.1",
       "nats": "1.4.9",
       "nodemon": "2.0.4",
  +    "nunjucks": "^3.2.1",
  ```

- Remove redundant testing tools:
  ```diff
       "imports-loader": "^0.7.0",
  -    "istanbul": "^0.4.5",
  ```
  (When using nyc which already depends on istanbul-lib-coverage)

Keep your testing infrastructure lean by regularly reviewing dependencies to ensure they're necessary, properly placed, and up-to-date.