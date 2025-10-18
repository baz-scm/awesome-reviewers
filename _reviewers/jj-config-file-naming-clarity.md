---
title: Config file naming clarity
description: 'Use descriptive, unambiguous names for configuration files to clearly
  indicate their scope and prevent user confusion about configuration hierarchy.


  When introducing new configuration files, especially in systems with multiple configuration
  layers (user, repo, workspace), choose names that explicitly indicate the scope
  rather than generic names that could...'
repository: jj-vcs/jj
label: Configurations
language: Rust
comments_count: 3
repository_stars: 21171
---

Use descriptive, unambiguous names for configuration files to clearly indicate their scope and prevent user confusion about configuration hierarchy.

When introducing new configuration files, especially in systems with multiple configuration layers (user, repo, workspace), choose names that explicitly indicate the scope rather than generic names that could be mistaken for broader configuration files.

For example, prefer `.jj/workspace-config.toml` over `.jj/config.toml` when the configuration is workspace-specific, as users might assume `.jj/config.toml` is the primary repository configuration file and overlook `.jj/repo/config.toml`.

```rust
// Good: Clear scope indication
let workspace_config_path = workspace_root.join(".jj").join("workspace-config.toml");
let repo_config_path = repo_root.join(".jj").join("repo").join("config.toml");

// Avoid: Ambiguous naming that could confuse users
let config_path = workspace_root.join(".jj").join("config.toml"); // Could be mistaken for main config
```

Consider the user's mental model when navigating configuration files. If multiple configuration files exist in the same conceptual space, their names should make the hierarchy and precedence clear at first glance. This reduces support burden and prevents configuration mistakes.