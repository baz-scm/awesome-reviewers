---
title: Global option placement
description: When an interface defines an option/parameter as *global* (i.e., it applies
  across subcommands or endpoints), pass it using the interface’s established parsing
  contract—even if it appears after a subcommand. Do not reorder flags “by intuition”
  if the interface specifies global semantics; instead, align with the documented/implemented
  behavior and then lock...
repository: microsoft/VSCode
label: API
language: Yaml
comments_count: 3
repository_stars: 194303
---

When an interface defines an option/parameter as *global* (i.e., it applies across subcommands or endpoints), pass it using the interface’s established parsing contract—even if it appears after a subcommand. Do not reorder flags “by intuition” if the interface specifies global semantics; instead, align with the documented/implemented behavior and then lock it in with CI validation (to catch argument-parsing errors early).

Example (Cargo CLI global `--config`):

```sh
# Valid when --config is a global option in the CLI contract
cargo build --config http.multiplexing=false --config net.retry=5 --release --target <target> --bin code

# Equivalent form (also acceptable)
cargo --config http.multiplexing=false --config net.retry=5 build --release --target <target> --bin code
```

Apply this standard to build/test/deploy scripts that act like “API clients”: keep configuration/options consistent across environments, and verify non-obvious placement or semantics in CI before relying on it in production pipelines.