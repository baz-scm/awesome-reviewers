---
title: Strategic dependency configuration
description: 'Configure dependencies in package.json strategically based on how they''re
  used in your project:


  1. **Direct dependencies** - Only for packages required for normal operation'
repository: nestjs/nest
label: Configurations
language: Json
comments_count: 5
repository_stars: 71766
---

Configure dependencies in package.json strategically based on how they're used in your project:

1. **Direct dependencies** - Only for packages required for normal operation
2. **Peer dependencies** - For lazy-loaded packages or optional integrations
3. **Optional peer dependencies** - Use peerDependenciesMeta to indicate optionality

```json
{
  "dependencies": {
    "core-package": "1.0.0"
  },
  "peerDependencies": {
    "lazy-loaded-package": ">=1.0.0",
    "axios": ">=0.18.0"
  },
  "peerDependenciesMeta": {
    "lazy-loaded-package": {
      "optional": true
    }
  }
}
```

For packages with 0.x versions (pre-1.0), use inclusive ranges (>=0.18.0) rather than caret ranges (^0.18.0) to allow compatible updates.

Avoid including type packages (@types/*) when the library already provides its own type definitions. For example, modern versions of Sequelize include built-in types, making @types/sequelize unnecessary.