---
title: Pin dependency versions
description: Always specify exact versions for dependencies and avoid pointing to
  moving targets like "master" branches or "latest" tags in configuration files. This
  ensures reproducible builds and prevents unexpected breakages when upstream dependencies
  change.
repository: facebook/yoga
label: Configurations
language: Other
comments_count: 2
repository_stars: 18255
---

Always specify exact versions for dependencies and avoid pointing to moving targets like "master" branches or "latest" tags in configuration files. This ensures reproducible builds and prevents unexpected breakages when upstream dependencies change.

When configuring dependencies across multiple components of a project, use consistent version numbers. For example, if your main project uses Kotlin 2.1.20, ensure all submodules and build configurations use the same version:

```gradle
// In build.gradle - use consistent versions
plugins {
    id("com.android.library") version "8.7.1" apply false
    id("com.android.application") version "8.7.1" apply false
    id 'org.jetbrains.kotlin.android' version '2.1.20' apply false // Match react-native version
}
```

```ruby
# In podspec files - pin to specific tags, not branches
spec.source = {
  :git => 'https://github.com/facebook/yoga.git',
  :tag => spec.version.to_s,  // Use tagged version
  # :branch => "master",      // Avoid this - causes unpredictable fetches
}
```

This practice prevents version drift, ensures all team members build with identical dependencies, and makes it easier to track which specific versions were used in each release.