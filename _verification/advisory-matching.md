---
title: "Advisory matching"
code: "V1015.001"
slug: "advisory-matching"
technique: "Dependency audit"
technique_id: "V1015"
technique_slug: "dependency-audit"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Compare resolved versions with OSV, GitHub and ecosystem advisories."
repos: 42
craft:
  - "Run an audit tool against the lockfile or manifest on every dependency change."
  - "Compare resolved versions with advisory databases such as OSV or the GitHub advisory database."
  - "Fail the build on advisories that have a fix available and report the rest."
reverse:
  - "A dependency-review workflow or audit step in CI for lockfile changes."
  - "An osv-scanner, deny.toml or pip-audit step in the pipeline."
packages:
  - id: "osv-scanner"
    name: "OSV-Scanner"
    url: "https://github.com/google/osv-scanner"
  - id: "pip-audit"
    name: "pip-audit"
    url: "https://github.com/pypa/pip-audit"
  - id: "govulncheck"
    name: "govulncheck"
    url: "https://github.com/golang/vuln"
  - id: "cargo-deny"
    name: "cargo-deny"
    url: "https://github.com/EmbarkStudios/cargo-deny"
  - id: "grype"
    name: "Grype"
    url: "https://github.com/anchore/grype"
tools:
  - name: "npm-audit"
    repos: 9
  - name: "pip-audit"
    repos: 2
  - name: "cargo-audit"
    repos: 2
  - name: "govulncheck"
    repos: 4
  - name: "cargo-deny"
    repos: 19
  - name: "dependency-review"
    repos: 12
examples:
  - repo: "nousresearch/hermes-agent"
    tool: "npm-audit"
    command: "npm audit --workspaces=false"
  - repo: "axios/axios"
    tool: "dependency-review"
    command: "uses actions/dependency-review-action"
  - repo: "mermaid-js/mermaid"
    tool: "dependency-review"
    command: "uses actions/dependency-review-action"
  - repo: "home-assistant/core"
    tool: "dependency-review"
    command: "uses actions/dependency-review-action"
  - repo: "earendil-works/pi"
    tool: "npm-audit"
    command: "npm audit signatures --omit=dev"
---
