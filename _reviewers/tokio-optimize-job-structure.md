---
title: Optimize job structure
description: Structure CI jobs for clarity, parallelism, and efficiency. Each job
  should have a single, well-defined purpose to prevent confusion about which tools
  and versions are being used.
repository: tokio-rs/tokio
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 28989
---

Structure CI jobs for clarity, parallelism, and efficiency. Each job should have a single, well-defined purpose to prevent confusion about which tools and versions are being used.

Key guidelines:
- Keep jobs focused on a single toolchain or task
- Split long-running jobs into parallel tasks
- Use performance-optimizing tools when available

For example, instead of:
```yaml
jobs:
  test-all:
    steps:
      - uses: dtolnay/rust-toolchain@stable
        with:
          toolchain: stable
      - uses: dtolnay/rust-toolchain@stable
        with:
          toolchain: nightly
      - name: Run multiple test suites
        run: |
          cargo test
          cargo miri test
```

Prefer:
```yaml
jobs:
  test-stable:
    steps:
      - uses: dtolnay/rust-toolchain@stable
        with:
          toolchain: stable
      - name: Run tests
        run: cargo test
        
  test-miri:
    steps:
      - uses: dtolnay/rust-toolchain@stable
        with:
          toolchain: nightly
          components: miri
      - uses: taiki-e/install-action@v2
        with:
          tool: cargo-nextest
      - name: Run miri tests
        run: cargo miri nextest run
```

This approach avoids confusion about which toolchain is being used for each command and allows jobs to run in parallel, significantly improving pipeline efficiency. Tests that were taking 37 minutes can be reduced to 21 minutes by using optimized tools like cargo-nextest.