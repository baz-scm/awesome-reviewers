---
title: Document build configurations
description: When setting Rust build configurations, especially in CI/Docker environments,
  explicitly document optimization choices and their tradeoffs. Consider whether configurations
  should live in Cargo.toml, .cargo/config.toml, or as environment variables in CI
  scripts. For Docker builds, document RUSTFLAGS options like optimization levels,
  relocation models, and...
repository: astral-sh/uv
label: Configurations
language: Dockerfile
comments_count: 2
repository_stars: 60322
---

When setting Rust build configurations, especially in CI/Docker environments, explicitly document optimization choices and their tradeoffs. Consider whether configurations should live in Cargo.toml, .cargo/config.toml, or as environment variables in CI scripts. For Docker builds, document RUSTFLAGS options like optimization levels, relocation models, and linking settings, along with their impact on binary size, performance, and security. Ensure consistency between Docker build commands and any custom profiles defined in project files.

```Dockerfile
# Document optimization choices and tradeoffs
ARG RUSTFLAGS="-C strip=symbols -C relocation-model=static -C target-feature=+crt-static -C opt-level=z"
# strip=symbols: Reduces binary size
# relocation-model=static: Reduces size at expense of ASLR security
# target-feature=+crt-static: Ensures fully static linking
# opt-level=z: Optimizes for size; benchmark to assess performance impact

# Ensure consistency with any custom profiles in Cargo.toml
RUN cargo build --release  # Uses custom profile if defined in Cargo.toml
```