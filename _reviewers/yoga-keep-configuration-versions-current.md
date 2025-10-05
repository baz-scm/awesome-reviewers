---
title: Keep configuration versions current
description: Regularly review and update version specifications in configuration files
  to align with current standards and internal practices. When updating versions,
  consider both the benefits of newer features and potential compatibility impacts.
repository: facebook/yoga
label: Configurations
language: Swift
comments_count: 2
repository_stars: 18255
---

Regularly review and update version specifications in configuration files to align with current standards and internal practices. When updating versions, consider both the benefits of newer features and potential compatibility impacts.

Configuration files should specify reasonably current versions of tools, languages, and frameworks rather than outdated minimums. However, version bumps should be planned carefully, especially for major version changes that might affect compatibility.

Ensure consistency across different build systems and package managers. If updating one configuration file, check related configurations to maintain alignment.

Example from Package.swift:
```swift
// Consider updating from older versions
swift-tools-version:5.3  // → swift-tools-version:5.8
cxxLanguageStandard: .cxx14  // → .cxx17 (when appropriate)

// Also check related configurations like CocoaPods
// to maintain consistency across build systems
```

Before updating, evaluate the trade-offs between staying current and maintaining stability, especially in widely-used libraries where breaking changes can impact many users.