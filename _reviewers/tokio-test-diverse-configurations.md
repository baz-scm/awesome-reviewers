---
title: Test diverse configurations
description: Configure test suites to run under multiple specialized environments
  to catch issues that might not appear in standard test runs. This includes testing
  with different compiler configurations, using specialized testing tools, and properly
  preserving environment variables when adding test-specific flags.
repository: tokio-rs/tokio
label: Testing
language: Yaml
comments_count: 2
repository_stars: 28989
---

Configure test suites to run under multiple specialized environments to catch issues that might not appear in standard test runs. This includes testing with different compiler configurations, using specialized testing tools, and properly preserving environment variables when adding test-specific flags.

Example:
```yaml
# In CI workflow
- name: Test with panic=abort
  run: |
    RUSTFLAGS="$RUSTFLAGS -C panic=abort -Zpanic-abort-tests" cargo test --workspace --all-features

- name: Test with memory safety analyzer
  run: |
    cargo miri test --features full --lib --tests --no-fail-fast
  env:
    MIRIFLAGS: -Zmiri-disable-isolation -Zmiri-strict-provenance
```

When adding new test environments, ensure you don't overwrite existing environment variables (append instead) and consider the maturity of experimental features when selecting testing configurations.