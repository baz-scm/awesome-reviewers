---
title: Cargo config in CI
description: When adjusting Cargo behavior for CI (especially network-related settings),
  apply configuration via Cargo’s CLI using `--config key=value` flags and keep it
  consistent across all Cargo subcommands (build, test, clippy).
repository: microsoft/VSCode
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 194303
---

When adjusting Cargo behavior for CI (especially network-related settings), apply configuration via Cargo’s CLI using `--config key=value` flags and keep it consistent across all Cargo subcommands (build, test, clippy).

Cargo treats `--config` as a global argument, so it’s safe to include it alongside subcommands in pipeline scripts; Cargo will merge these into the effective configuration.

Example (repeat the same pattern across clippy/build/test steps):

```sh
cargo test \
  --config http.multiplexing=false \
  --config net.retry=5 \
  --locked

cargo build \
  --config http.multiplexing=false \
  --config net.retry=5 \
  --release \
  --target "$TARGET" \
  --bin code

cargo clippy \
  --config http.multiplexing=false \
  --config net.retry=5 \
  --all-targets \
  --locked \
  -- -D warnings
```

Standardize these flags so developers don’t end up with different CI outcomes depending on which job or step they used.