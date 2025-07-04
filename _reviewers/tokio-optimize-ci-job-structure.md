---
title: Optimize CI job structure
description: 'Structure your CI workflows to maximize performance and clarity. Each
  job should have a single, clear responsibility with these guidelines:


  1. **One toolchain per job**: Keep jobs focused with a single Rust toolchain version
  per job. Multiple toolchains in one job create confusion about which version is
  being used for each command.'
repository: tokio-rs/tokio
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 28981
---

Structure your CI workflows to maximize performance and clarity. Each job should have a single, clear responsibility with these guidelines:

1. **One toolchain per job**: Keep jobs focused with a single Rust toolchain version per job. Multiple toolchains in one job create confusion about which version is being used for each command.
   
   ```yml
   # Don't do this:
   - name: Install Rust stable
     uses: dtolnay/rust-toolchain@stable
     with:
         toolchain: ${{ env.rust_stable }}
   - name: Install Rust nightly
     uses: dtolnay/rust-toolchain@stable
     with:
         toolchain: ${{ env.rust_nightly }}
   ```

   Instead, create separate jobs for different toolchains or requirements.

2. **Split long-running tasks**: Divide lengthy operations into separate jobs that can run in parallel. When a job begins taking too much time (like Miri tests), split it to enable faster feedback cycles and better resource utilization.

3. **Use efficient testing tools**: Employ optimized testing tools like cargo-nextest to significantly reduce execution time. For example, replacing standard test runners with nextest can reduce CI runtime by 40% or more, as seen with Miri jobs (37 minutes → 21 minutes).

These practices will result in more maintainable CI configurations, faster feedback for developers, and clearer error identification when builds fail.