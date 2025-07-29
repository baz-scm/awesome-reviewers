---
title: organize test scripts properly
description: Keep base test scripts generic and create specialized variants for specific
  workflows. Base scripts like "test" should remain simple and flexible, allowing
  developers to pass additional arguments via CLI. For specialized workflows, create
  separate scripts with descriptive names.
repository: remix-run/react-router
label: Testing
language: Json
comments_count: 2
repository_stars: 55270
---

Keep base test scripts generic and create specialized variants for specific workflows. Base scripts like "test" should remain simple and flexible, allowing developers to pass additional arguments via CLI. For specialized workflows, create separate scripts with descriptive names.

For example, instead of modifying the base test script:
```json
{
  "scripts": {
    "test": "jest --projects packages/react-router --watch"
  }
}
```

Keep the base script generic and create specialized variants:
```json
{
  "scripts": {
    "test": "jest",
    "test:integration": "pnpm build && pnpm test:integration:run",
    "test:integration:run": "pnpm playwright:integration"
  }
}
```

This approach allows developers to use `npm test -- --projects packages/react-router --watch` for custom CLI arguments while providing convenient shortcuts for common workflows. It also enables iterative testing without unnecessary rebuilds by separating build and execution steps.