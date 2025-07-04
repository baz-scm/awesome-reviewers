---
title: Test production configurations too
description: Include testing configurations that mirror production environments to
  catch issues that might only manifest in release builds. For example, testing with
  panic=abort can reveal issues that wouldn't appear when testing with the default
  panic=unwind setting. Similarly, when using specialized testing tools like Miri,
  configure the appropriate flags to ensure...
repository: tokio-rs/tokio
label: Testing
language: Yaml
comments_count: 2
repository_stars: 28981
---

Include testing configurations that mirror production environments to catch issues that might only manifest in release builds. For example, testing with panic=abort can reveal issues that wouldn't appear when testing with the default panic=unwind setting. Similarly, when using specialized testing tools like Miri, configure the appropriate flags to ensure comprehensive validation under realistic conditions.

Example:
```yaml
- name: test all --all-features panic=abort
  run: |
    RUSTFLAGS="$RUSTFLAGS -C panic=abort -Zpanic-abort-tests" cargo nextest run --workspace --all-features --tests
```

When adding new test configurations, always preserve existing environment variables by appending to them rather than replacing them entirely, which ensures that other important configurations remain intact.