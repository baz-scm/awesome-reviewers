---
title: "Compiler as checker"
code: "V1006.003"
slug: "compiler-as-checker"
technique: "Type checking"
technique_id: "V1006"
technique_slug: "type-checking"
tactic: "Static analysis"
tactic_id: "VA02"
description: "In compiled languages the build is the type check; a failing build is this check failing."
repos: 21
craft:
  - "Make the build step in CI the gate for type errors in compiled code."
  - "Run cargo check on pull requests for a fast type-only pass."
  - "Keep compiler warnings as errors in CI so type issues stop the pipeline."
reverse:
  - "A CI job that runs cargo build or cargo check and fails the pipeline on error."
  - "Compiler flags such as -Werror or RUSTFLAGS set in CI configuration."
packages: []
tools:
  - name: "cargo-check"
    repos: 21
examples:
  - repo: "facebook/react"
    tool: "cargo-check"
    command: "cargo check"
  - repo: "oven-sh/bun"
    tool: "cargo-check"
    command: "cargo check --workspace --all-targets --keep-going"
  - repo: "warpdotdev/warp"
    tool: "cargo-check"
    command: "cargo check --locked -p warp --lib --features agent_mode_evals"
  - repo: "aaif-goose/goose"
    tool: "cargo-check"
    command: "cargo check --locked --target wasm32-unknown-unknown -p goose-agent -p goose-provider-types"
  - repo: "ruvnet/ruflo"
    tool: "cargo-check"
    command: "cargo check --features native --verbose"
---
