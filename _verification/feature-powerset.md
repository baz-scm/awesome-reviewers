---
title: "Feature powerset"
code: "V1024.002"
slug: "feature-powerset"
technique: "Version and platform matrix"
technique_id: "V1024"
technique_slug: "version-and-platform-matrix"
tactic: "Testing"
tactic_id: "VA04"
description: "Build and test each combination of optional features or extras."
repos: 4
craft:
  - "Run cargo hack with --feature-powerset in CI, bounding cost with --depth if needed."
  - "Exclude feature combinations that cannot build, with a reason in the config."
  - "Run the test suite for each combination that builds."
reverse:
  - "cargo hack --feature-powerset steps in a workflow file."
  - "Feature lists in Cargo.toml with exclude or depth settings in the CI command."
  - "CI logs that show one run per feature combination."
packages:
  - id: "cargo-hack"
    name: "cargo-hack"
    url: "https://github.com/taiki-e/cargo-hack"
tools:
  - name: "cargo-hack"
    repos: 4
examples:
  - repo: "pola-rs/polars"
    tool: "cargo-hack"
    command: "cargo hack check -p polars --each-feature --no-dev-deps"
  - repo: "juspay/hyperswitch"
    tool: "cargo-hack"
    command: "cargo hack check --workspace --each-feature --all-targets --exclude-features v2 payment_v2"
  - repo: "tokio-rs/tokio"
    tool: "cargo-hack"
    command: "cargo hack test --each-feature"
  - repo: "tokio-rs/axum"
    tool: "cargo-hack"
    command: "cargo hack check --each-feature --no-dev-deps --all"
---
