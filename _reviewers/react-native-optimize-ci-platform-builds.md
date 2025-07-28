---
title: Optimize CI platform builds
description: When configuring CI/CD build pipelines, limit builds to only the platforms
  your project actively supports and avoid building for out-of-tree (OOT) platforms
  that maintain separate forks. This reduces unnecessary CI overhead and build times.
  Additionally, design your build configuration to support parallelization by allowing
  platforms to be passed as...
repository: facebook/react-native
label: CI/CD
language: JavaScript
comments_count: 2
repository_stars: 123178
---

When configuring CI/CD build pipelines, limit builds to only the platforms your project actively supports and avoid building for out-of-tree (OOT) platforms that maintain separate forks. This reduces unnecessary CI overhead and build times. Additionally, design your build configuration to support parallelization by allowing platforms to be passed as separate parameters.

For example, instead of building for all possible platforms, focus on core supported platforms:

```javascript
// Only build for actively supported platforms
const supportedPlatforms = ['iOS', 'iOS simulator', 'macOS,variant=Mac Catalyst'];

// Design for parallel execution in CI
const buildPlatform = (platform) => {
  const buildCommand = `xcodebuild -scheme React -destination "generic/platform=${platform}" ...`;
  // Build logic here
};

// Can be parallelized in CI by passing platforms separately
supportedPlatforms.forEach(buildPlatform);
```

This approach improves CI efficiency by avoiding builds for platforms that won't be used while maintaining the flexibility to parallelize builds across the platforms that matter.