---
title: Synchronize configuration files
description: Ensure all related configuration files are updated consistently when
  making changes to dependencies, versions, or other configuration settings. When
  updating a dependency version in one file (e.g., package.json), ensure that all
  related files (e.g., lockfiles, version specifications) are also updated to maintain
  consistency. This prevents subtle integration...
repository: rust-lang/rust
label: Configurations
language: Json
comments_count: 2
repository_stars: 105254
---

Ensure all related configuration files are updated consistently when making changes to dependencies, versions, or other configuration settings. When updating a dependency version in one file (e.g., package.json), ensure that all related files (e.g., lockfiles, version specifications) are also updated to maintain consistency. This prevents subtle integration issues and build failures.

Example:
```
// When updating package.json
{
  "dependencies": {
    "browser-ui-test": "0.21.1",  // Updated from 0.20.6
    // other dependencies...
  }
}

// Also update related files like browser-ui-test.version to match
```

For build configurations, consider separating build artifacts from source code by copying configuration files to the build directory and running commands from there. This maintains source directory immutability during builds.