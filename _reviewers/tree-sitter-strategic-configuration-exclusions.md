---
title: Strategic configuration exclusions
description: When configuring build exclusions in package manifests or configuration
  files, be strategic and minimal. Only exclude files that cause actual build issues
  (like non-source files that generate compilation warnings), while preserving important
  files such as licenses and directories that may be relevant for future features.
  Modern tooling often handles file...
repository: tree-sitter/tree-sitter
label: Configurations
language: Swift
comments_count: 2
repository_stars: 21799
---

When configuring build exclusions in package manifests or configuration files, be strategic and minimal. Only exclude files that cause actual build issues (like non-source files that generate compilation warnings), while preserving important files such as licenses and directories that may be relevant for future features. Modern tooling often handles file filtering automatically, so explicit exclusion lists may be unnecessary.

For example, in Package.swift:
```swift
.target(name: "TreeSitter",
        path: "lib",
        exclude: [
          // Only exclude files that cause build warnings
          "src/unicode/ICU_SHA",
          "src/unicode/README.md", 
          "src/unicode/LICENSE",
          // Don't exclude "src/wasm" - may be needed for future support
        ],
```

Before adding exclusions, verify they solve actual build problems rather than preemptively excluding files that might seem irrelevant. Consider whether newer versions of your build tools can handle the filtering automatically.