---
title: "License policy"
code: "V1015.003"
slug: "license-policy"
technique: "Dependency audit"
technique_id: "V1015"
technique_slug: "dependency-audit"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Allow or deny dependencies by license."
repos: 31
craft:
  - "Write an allow list of licenses in the policy file."
  - "Deny any dependency whose license is not on the list and fail the check."
  - "Run the license check on every dependency change."
reverse:
  - "A deny.toml with a [licenses] section listing allowed licenses."
  - "A dependency-review step configured with allowed or denied license values."
packages:
  - id: "cargo-deny"
    name: "cargo-deny"
    url: "https://github.com/EmbarkStudios/cargo-deny"
tools:
  - name: "cargo-deny"
    repos: 19
  - name: "dependency-review"
    repos: 12
examples:
  - repo: "axios/axios"
    tool: "dependency-review"
    command: "uses actions/dependency-review-action"
  - repo: "mermaid-js/mermaid"
    tool: "dependency-review"
    command: "uses actions/dependency-review-action"
  - repo: "home-assistant/core"
    tool: "dependency-review"
    command: "uses actions/dependency-review-action"
  - repo: "zed-industries/zed"
    tool: "dependency-review"
    command: "uses actions/dependency-review-action"
  - repo: "astral-sh/uv"
    tool: "cargo-deny"
    command: "cargo deny --all-features check licenses"
---
