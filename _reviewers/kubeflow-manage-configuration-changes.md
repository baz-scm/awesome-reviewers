---
title: Manage configuration changes
description: 'Carefully manage configuration file changes to ensure consistency and
  minimize unintended impacts across your project. When modifying configuration files:'
repository: kubeflow/kubeflow
label: Configurations
language: Json
comments_count: 3
repository_stars: 15064
---

Carefully manage configuration file changes to ensure consistency and minimize unintended impacts across your project. When modifying configuration files:

1) Ensure compiler settings match runtime requirements - update targets to support required language features (like changing TypeScript target to "es2020" to support BigInt in Node.js 12)

2) Maintain consistent paths and settings across related configurations to prevent deployment issues

```json
// Example: Consistent paths in build scripts
"scripts": {
  "start": "ng serve --base-href /tensorboards/ --deploy-url /tensorboards/",
  "build": "ng build --prod --base-href /tensorboards/ --deploy-url static/"
}
```

3) Isolate high-impact configuration changes (like dependency updates that affect package-lock.json) into separate PRs to maintain reviewability and minimize unintended side effects
