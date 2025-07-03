---
title: Dependency classification standards
description: Properly classify dependencies in package.json according to their usage
  pattern and project guidelines. This ensures correct build behavior, optimizes package
  size, and prevents dependency conflicts.
repository: langchain-ai/langchainjs
label: Configurations
language: Json
comments_count: 4
repository_stars: 15004
---

Properly classify dependencies in package.json according to their usage pattern and project guidelines. This ensures correct build behavior, optimizes package size, and prevents dependency conflicts.

- **Direct dependencies**: Include only packages required at runtime
- **Peer dependencies**: Use for optional integrations (also add as dev dependencies for testing)
- **Dev dependencies**: Use for packages only needed during development/testing
- **Avoid unnecessary dependencies**: Don't add packages for functionality available natively

Example of correct dependency classification:
```json
// package.json
{
  "dependencies": {
    // Only runtime requirements
  },
  "peerDependencies": {
    "@libsql/client": "^0.14.0" // Optional integration
  },
  "devDependencies": {
    "@libsql/client": "^0.14.0", // Also needed for testing
    "@cloudflare/workers-types": "^4.20240502.0" // Types only
  }
}
```

For third-party integrations, follow the project's integration guidelines to determine the appropriate dependency type. Avoid adding dependencies when equivalent functionality exists natively.
