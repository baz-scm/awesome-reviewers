---
title: environment loading order
description: Environment files and variables must be loaded before creating any factories,
  services, or components that depend on them. This ensures that environment-based
  configuration propagates correctly throughout the application lifecycle.
repository: denoland/deno
label: Configurations
language: Rust
comments_count: 3
repository_stars: 103714
---

Environment files and variables must be loaded before creating any factories, services, or components that depend on them. This ensures that environment-based configuration propagates correctly throughout the application lifecycle.

Load environment files early in the initialization sequence, before creating factories or services that read environment variables. Additionally, clean up sensitive environment variables after reading to prevent unintended propagation to subprocesses.

Example of correct ordering:
```rust
// Load environment file first
load_env_variables_from_env_file(
  flags.env_file,
  log_level,
);

// Then create factory (which may read env vars)
let factory = create_factory()?;
let cli_options = factory.cli_options()?;

// Clean up sensitive env vars after reading
let control_sock = std::env::var("DENO_CONTROL_SOCK")?;
std::env::remove_var("DENO_CONTROL_SOCK"); // Prevent subprocess propagation
```

Avoid using `.env()` in CLI argument definitions since the environment file hasn't been processed yet at argument parsing time. Instead, read environment variables after the environment file has been loaded and apply them to the appropriate configuration structures.