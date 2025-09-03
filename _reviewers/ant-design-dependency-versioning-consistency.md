---
title: Dependency versioning consistency
description: Establish and maintain consistent dependency versioning strategies in
  package.json configuration. Choose between caret (^) and tilde (~) ranges based
  on stability requirements and update policies. For stable production dependencies,
  prefer tilde ranges to avoid unexpected breaking changes, while development dependencies
  can use caret ranges for latest...
repository: ant-design/ant-design
label: Configurations
language: Json
comments_count: 6
repository_stars: 95882
---

Establish and maintain consistent dependency versioning strategies in package.json configuration. Choose between caret (^) and tilde (~) ranges based on stability requirements and update policies. For stable production dependencies, prefer tilde ranges to avoid unexpected breaking changes, while development dependencies can use caret ranges for latest features. Regularly review and update dependency versions to stay current with security patches and improvements.

Example:
```json
{
  "dependencies": {
    "enter-animation": "~0.1.1",
    "@rc-component/form": "~1.2.0"
  },
  "devDependencies": {
    "tsx": "^4.20.3",
    "terser": "~5.42.0"
  }
}
```

For tools with known stability issues, lock to specific versions until fixes are available, as seen with "@biomejs/cli-darwin-arm64": "2.0.0".