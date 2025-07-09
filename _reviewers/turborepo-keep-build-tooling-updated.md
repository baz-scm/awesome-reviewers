---
title: Keep build tooling updated
description: Maintain up-to-date build and CI/CD tooling to leverage the latest features,
  performance improvements, and security patches. Regularly check for updates to build
  orchestration tools like Turborepo and use provided codemods for seamless upgrades.
  When configuring build pipelines, optimize task dependencies by using topological
  approaches (like Turborepo's...
repository: vercel/turborepo
label: CI/CD
language: Json
comments_count: 4
repository_stars: 28115
---

Maintain up-to-date build and CI/CD tooling to leverage the latest features, performance improvements, and security patches. Regularly check for updates to build orchestration tools like Turborepo and use provided codemods for seamless upgrades. When configuring build pipelines, optimize task dependencies by using topological approaches (like Turborepo's `topo` mode) to enable more efficient parallel execution. Additionally, when adding new scripts to your workflow, ensure proper execution order by establishing clear dependencies between build steps.

Example:
```json
{
  "name": "project",
  "devDependencies": {
    "turbo": "^2.0.0"  // Using latest major version
  },
  "scripts": {
    "upgrade-turbo": "npx @turbo/codemod upgrade",
    "build": "turbo run build",
    "preview-storybook": "turbo run build preview-storybook" // Ensuring build runs first
  },
  "turbo": {
    "pipeline": {
      "test": {
        "dependsOn": ["^test"],
        "dependencyMode": "topo" // Only block on actual dependencies
      }
    }
  }
}
```