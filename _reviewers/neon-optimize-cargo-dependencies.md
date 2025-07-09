---
title: Optimize cargo dependencies
description: 'Maintain clean and efficient dependency configurations in Cargo.toml
  files by following these practices:


  1. **Use workspace inheritance** when available for common settings and dependencies:'
repository: neondatabase/neon
label: Configurations
language: Toml
comments_count: 6
repository_stars: 19015
---

Maintain clean and efficient dependency configurations in Cargo.toml files by following these practices:

1. **Use workspace inheritance** when available for common settings and dependencies:
   ```toml
   [package]
   name = "your_package"
   version = "0.1.0"
   edition.workspace = true
   license.workspace = true

   [dependencies]
   some_dependency.workspace = true
   ```

2. **Remove unused dependencies** to keep builds efficient and prevent unnecessary bloat.

3. **Maintain alphabetical ordering** of dependencies to improve readability and make changes easier to track.

4. **Avoid duplicate version specifications** when a dependency is already defined in the workspace. Use the workspace version unless you specifically need a different version:
   ```toml
   # Prefer this
   tokio-util.workspace = true
   
   # Instead of this
   tokio-util = { version = "0.7", features = ["compat"] }
   ```

5. **When upgrading a dependency version**, ensure compatibility with existing code and consider whether the upgrade should happen at the workspace level.

Following these practices helps maintain a clean dependency tree, reduces build times, and makes configuration files easier to understand and maintain.