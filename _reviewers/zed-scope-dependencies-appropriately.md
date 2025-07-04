---
title: Scope dependencies appropriately
description: 'Configure dependencies with their minimum necessary scope to maintain
  clean architecture and improve build times. Key practices:


  1. **Test-only dependencies should be dev-dependencies**'
repository: zed-industries/zed
label: Configurations
language: Toml
comments_count: 5
repository_stars: 62119
---

Configure dependencies with their minimum necessary scope to maintain clean architecture and improve build times. Key practices:

1. **Test-only dependencies should be dev-dependencies**
   If a dependency is only used for tests, add it as a dev-dependency and use `#[cfg(test)]` annotations:
   ```rust
   // Instead of adding to main Cargo.toml
   // unicode-width = "0.2"
   
   // Add to [dev-dependencies] section instead
   // And restrict usage to test code:
   #[cfg(test)]
   use unicode_width::UnicodeWidthStr;
   ```

2. **Keep core modules lightweight**
   Don't add heavy dependencies to utility or core modules. Move dependent code to appropriate modules:
   ```rust
   // Instead of this in util/Cargo.toml:
   // schemars.workspace = true
   
   // Create plain enums in util:
   pub enum SortStrategy {
       Lexicographical,
       Alphabetical,
   }
   
   // Then convert in settings module where JsonSchema is available
   ```

3. **Scope feature flags correctly**
   Define features at the appropriate module level rather than globally. For workspace-wide features, manage them centrally:
   ```toml
   # In workspace Cargo.toml:
   tokio = { version = "1.0", features = ["rt", "rt-multi-thread"] }
   
   # In module Cargo.toml:
   tokio.workspace = true
   ```

4. **Extract global configuration changes**
   When changing dependency configurations that affect multiple modules, consider making it a separate PR to properly evaluate the impact.