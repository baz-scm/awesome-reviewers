---
title: Parameterize build processes
description: 'When designing build scripts for multi-package repositories, use parameterization
  to handle special cases rather than creating duplicate scripts with minor variations.
  This approach maintains consistency while accommodating package-specific needs.
  For example, instead of hardcoding different behaviors, add flags that can modify
  behavior:'
repository: mui/material-ui
label: CI/CD
language: Json
comments_count: 2
repository_stars: 96063
---

When designing build scripts for multi-package repositories, use parameterization to handle special cases rather than creating duplicate scripts with minor variations. This approach maintains consistency while accommodating package-specific needs. For example, instead of hardcoding different behaviors, add flags that can modify behavior:

```json
"scripts": {
  "build": "standard-build-script --skipEsmPkg",
  "build:esm-pkg": "node ./scripts/create-esm-package-json.mjs"
}
```

Similarly, prefer built-in parameterization of tools (like pnpm's `--dry-run` flag) over custom implementations for common CI/CD operations. This improves maintainability and leverages well-tested functionality.