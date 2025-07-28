---
title: dependency management strategy
description: 'When configuring dependencies in package.json, follow these strategic
  principles to ensure stable and maintainable package management:


  **Peer Dependencies**: Use peer dependencies judiciously to enable proper package
  hoisting while avoiding forced installations for all consumers. As noted: "We still
  need it here for it to be hoisted correctly. But we can...'
repository: facebook/react-native
label: Configurations
language: Json
comments_count: 4
repository_stars: 123178
---

When configuring dependencies in package.json, follow these strategic principles to ensure stable and maintainable package management:

**Peer Dependencies**: Use peer dependencies judiciously to enable proper package hoisting while avoiding forced installations for all consumers. As noted: "We still need it here for it to be hoisted correctly. But we can make it optional and make it a direct dependency in the template." Consider making peer dependencies optional when appropriate and satisfy requirements through direct dependencies in consuming packages.

**Version Locking**: Lock critical dependencies to specific versions that are known to work, especially for testing and tooling packages. Avoid using loose version ranges for packages that frequently introduce breaking changes. This prevents situations where "updates break testing" and ensures consistent behavior across environments.

**Local vs Global Dependencies**: Prefer local package dependencies over global installations to ensure reproducible builds and proper dependency resolution. Instead of requiring global installations, include dependencies directly in package.json: "You don't need to install globally if installing here."

**Minimize Changes During Migrations**: During monorepo transitions or major refactoring, "limit the changes to those packages to only the necessary ones" to reduce complexity and potential issues.

Example of proper dependency configuration:
```json
{
  "peerDependencies": {
    "@react-native-community/cli-server-api": "*"
  },
  "peerDependenciesMeta": {
    "@react-native-community/cli-server-api": {
      "optional": true
    }
  },
  "devDependencies": {
    "appium": "2.0.0",
    "appium-uiautomator2-driver": "^2.29.0"
  }
}
```