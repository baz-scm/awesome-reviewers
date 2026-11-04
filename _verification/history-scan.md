---
title: "History scan"
code: "V1008.002"
slug: "history-scan"
technique: "Secret scanning"
technique_id: "V1008"
technique_slug: "secret-scanning"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Scan full git history, since deleting a secret in a later commit does not remove it."
repos: 7
craft:
  - "Run the scanner once over the full git history."
  - "Rotate every credential found, even if a later commit removed it."
  - "Re-run the history scan on a schedule, not only on pull requests."
reverse:
  - "A scheduled CI workflow that scans full history with gitleaks or trufflehog."
  - "Allow-list entries that name a reviewed historic commit hash."
  - "A rotation record or incident note for each historic finding."
packages:
  - id: "gitleaks"
    name: "Gitleaks"
    url: "https://github.com/gitleaks/gitleaks"
  - id: "trufflehog"
    name: "TruffleHog"
    url: "https://github.com/trufflesecurity/trufflehog"
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
