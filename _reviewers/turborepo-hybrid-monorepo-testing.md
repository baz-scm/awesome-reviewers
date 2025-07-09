---
title: Hybrid monorepo testing
description: When working with tests in a monorepo, implement a hybrid testing approach
  that balances local development experience with CI performance. Set up local Vitest
  configurations in each package while also configuring a root workspace for unified
  testing. This preserves Turborepo's caching benefits in CI while providing a better
  developer experience.
repository: vercel/turborepo
label: Testing
language: Other
comments_count: 2
repository_stars: 28115
---

When working with tests in a monorepo, implement a hybrid testing approach that balances local development experience with CI performance. Set up local Vitest configurations in each package while also configuring a root workspace for unified testing. This preserves Turborepo's caching benefits in CI while providing a better developer experience.

Always explicitly specify coverage outputs in your Turborepo configuration:

```json
{
  "tasks": {
    "test": {
      "dependsOn": ["^test", "@repo/vitest-config#build"],
      "outputs": ["coverage/**"]  // Explicitly define coverage output paths
    },
    "merge-json-reports": {
      "inputs": ["coverage/raw/**"],
      "outputs": ["coverage/merged/**"]
    },
    "report": {
      "dependsOn": ["merge-json-reports"],
      "inputs": ["coverage/merge"],
      "outputs": ["coverage/report/**"]
    }
  }
}
```

This approach enables you to efficiently run tests locally during development while maintaining proper caching for CI environments and generating comprehensive coverage reports that can be merged across packages.