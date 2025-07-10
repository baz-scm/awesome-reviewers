---
title: Standard configuration files
description: Use standardized, tool-specific configuration files instead of embedding
  configurations in CI scripts or other build files. This improves discoverability,
  ensures consistency between local development and CI environments, and provides
  self-documentation for required settings.
repository: maplibre/maplibre-native
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 1411
---

Use standardized, tool-specific configuration files instead of embedding configurations in CI scripts or other build files. This improves discoverability, ensures consistency between local development and CI environments, and provides self-documentation for required settings.

However, be mindful of introducing dependencies on specific tooling ecosystems. Ensure your configuration approach works well with all build systems your project might interact with.

Example:
```yaml
# Instead of this in a CI workflow file:
- name: Add targets for Rust toolchain
  run: rustup target add --toolchain stable-x86_64-unknown-linux-gnu aarch64-linux-android

# Use a standard configuration file (rust-toolchain.toml):
# [toolchain]
# targets = ["aarch64-linux-android", "armv7-linux-androideabi"]
```

This approach documents required settings in conventional locations that tools automatically recognize, reducing the need for extra documentation while ensuring consistency across environments.