---
title: "Pre-commit secret scan"
code: "V1008.001"
slug: "pre-commit-secret-scan"
technique: "Secret scanning"
technique_id: "V1008"
technique_slug: "secret-scanning"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Block the commit locally, before the secret reaches a remote."
repos: 7
craft:
  - "Add the gitleaks or detect-secrets hook to .pre-commit-config.yaml."
  - "Commit the scanner config that holds the allow-list rules."
  - "Run the same scanner and config in CI so local and remote results match."
reverse:
  - "A gitleaks or detect-secrets hook id in .pre-commit-config.yaml."
  - "A .gitleaks.toml or .secrets.baseline file at the repository root."
  - "A CI job that runs gitleaks with the repository config."
packages:
  - id: "gitleaks"
    name: "Gitleaks"
    url: "https://github.com/gitleaks/gitleaks"
  - id: "detect-secrets"
    name: "detect-secrets"
    url: "https://github.com/Yelp/detect-secrets"
tools:
  - name: "gitleaks"
    repos: 7
examples:
  - repo: "cline/cline"
    tool: "gitleaks"
    command: "gitleaks git --pre-commit --redact --staged --verbose"
  - repo: "awslabs/mcp"
    tool: "gitleaks"
    command: "pre-commit hook gitleaks"
  - repo: "maximhq/bifrost"
    tool: "gitleaks"
    command: "pre-commit hook gitleaks"
  - repo: "snyk/cli"
    tool: "gitleaks"
    command: "pre-commit hook gitleaks"
  - repo: "awslabs/aidlc-workflows"
    tool: "gitleaks"
    command: "gitleaks version"
---
