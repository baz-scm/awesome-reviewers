---
title: Document versioning strategies
description: 'Establish and clearly document versioning strategies in configuration
  files, both for your application and its dependencies. For application versioning,
  include detailed explanations of each component in the version string:'
repository: influxdata/influxdb
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 30268
---

Establish and clearly document versioning strategies in configuration files, both for your application and its dependencies. For application versioning, include detailed explanations of each component in the version string:

```
v3.M.m-B[.Q.q.b]  # eg, v3.0.0-0.beta.1.0 or v3.0.0-1
 | | | |  | | |
 | | | |  | |  ----------> package build number for 'quality'
 | | | |  |  ------------> 'quality' release number
 | | | |   --------------> release quality (optional: alpha, beta, rc)
 | | |  -----------------> package build number
 | |  -------------------> micro version (non-breaking changes)
 |  ---------------------> minor version (breaking changes)
  -----------------------> major version (hugely breaking changes)
```

For dependencies in CI/CD configurations, make deliberate decisions about whether to pin specific versions (`tool@v1.2.3`) or use floating references (`tool@latest`). Document the reasoning behind your choice, and regularly review dependencies with floating versions to ensure they remain stable. When using `@latest`, verify that upstream maintainers handle versioning responsibly to prevent unexpected breaking changes in your build pipeline.