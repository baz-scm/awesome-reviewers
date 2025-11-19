---
title: Document CI configuration clearly
description: Always include file path comments in CI configuration code blocks and
  use officially recommended setup actions for CI tools. This improves documentation
  clarity and ensures reliable CI pipeline configuration.
repository: nrwl/nx
label: CI/CD
language: Other
comments_count: 6
repository_stars: 27518
---

Always include file path comments in CI configuration code blocks and use officially recommended setup actions for CI tools. This improves documentation clarity and ensures reliable CI pipeline configuration.

When showing configuration examples, add file path comments to help developers understand where the code belongs:

```yaml
# .github/workflows/ci.yml
name: CI
jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - run: npx nx affected -t lint test build
```

```javascript
// module-federation.config.ts
export default {
    remotes: [
        ['shop', 'https://shop.example.com'],
        ['cart', 'https://cart.example.com'],
    ]
}
```

Additionally, prefer official tool setup actions over custom alternatives. For example, continue using `pnpm/action-setup@v4` for pnpm projects since that's what the official documentation recommends, rather than implementing custom setup steps.

This approach reduces confusion about file locations, makes configurations easier to implement correctly, and ensures compatibility with tool updates and best practices.