---
title: Standardize dependency version notation
description: 'When specifying dependencies in package.json, follow consistent version
  notation patterns that align with your project''s stability and compatibility requirements:'
repository: expressjs/express
label: Configurations
language: Json
comments_count: 7
repository_stars: 67300
---

When specifying dependencies in package.json, follow consistent version notation patterns that align with your project's stability and compatibility requirements:

1. Choose the appropriate notation based on your project type:
   - Use caret notation (`^`) for libraries that properly follow semver when you want to receive compatible updates automatically
   - Use tilde notation (`~`) for patch-level updates only
   - Use exact versions (without prefix) for critical dependencies where any change might introduce risks

2. Maintain consistency across the project and document your versioning strategy in contributing guidelines.

3. Consider backward compatibility with older npm versions and user environments when selecting notation style.

Example:
```json
{
  "dependencies": {
    "express": "^4.18.2",     // Library following semver - accepts compatible updates
    "body-parser": "~1.20.1", // Accepts patch updates only
    "crypto-library": "2.0.1" // Exact version for critical security dependency
  },
  "engines": {
    "node": "^14 || ^16 || ^18 || ^20" // Clear specification of supported versions
  }
}
```

Remember that some projects may have strict policies prohibiting certain notation types based on their ecosystem requirements. Always follow project-specific guidelines when they exist.