---
title: Configuration naming consistency
description: Ensure configuration elements (environment variables, feature flags,
  config files) maintain consistent naming and clear documentation across code, logs,
  and documentation. Mismatched names between implementation and logging/documentation
  create confusion and debugging difficulties.
repository: snyk/cli
label: Configurations
language: JavaScript
comments_count: 3
repository_stars: 5178
---

Ensure configuration elements (environment variables, feature flags, config files) maintain consistent naming and clear documentation across code, logs, and documentation. Mismatched names between implementation and logging/documentation create confusion and debugging difficulties.

When working with configuration:
- Use identical names in code, environment variables, logs, and documentation
- Add clear comments explaining the purpose of configuration wrappers or compatibility functions
- Ensure feature flags and configuration parameters are properly propagated through function calls

Example of inconsistent naming to avoid:
```javascript
// Code uses SNYK_CONFIG_FILE but logs reference TEST_CONFIG_FILE
if (!process.env.SNYK_CONFIG_FILE && !process.env.TEST_CONFIG_FILE) {
  // ...
}
console.info('Snyk configuration [TEST_CONFIG_FILE] ...' + process.env.SNYK_CONFIG_FILE);
```

Example of proper configuration handling:
```javascript
// Wrapper for CommonJS compatibility
async function callModule(mod, args) {
  // Clear documentation of purpose
}

function run(root, options, featureFlags) {
  // Properly propagate configuration parameters
  validateProjectType(options, projectType, featureFlags);
  return runTest(projectType, root, options, featureFlags);
}
```