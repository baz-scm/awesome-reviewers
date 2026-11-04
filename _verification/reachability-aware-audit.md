---
title: "Reachability-aware audit"
code: "V1015.002"
slug: "reachability-aware-audit"
technique: "Dependency audit"
technique_id: "V1015"
technique_slug: "dependency-audit"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Report a vulnerable dependency only when the vulnerable function is called."
repos: 4
craft:
  - "Run govulncheck on the module so it reports only vulnerabilities in functions the code calls."
  - "Read the call path in each report before upgrading the dependency."
  - "Run it in CI on pull requests and on a daily schedule."
reverse:
  - "A govulncheck step in CI or a script target that runs govulncheck on the module."
  - "go.mod and go.sum files with the vulnerability check wired into the pipeline."
packages:
  - id: "govulncheck"
    name: "govulncheck"
    url: "https://github.com/golang/vuln"
tools:
  - name: "govulncheck"
    repos: 4
examples:
  - repo: "prometheus/prometheus"
    tool: "govulncheck"
    command: "uses golang/govulncheck-action"
  - repo: "apache/airflow"
    tool: "govulncheck"
    command: "govulncheck ./..."
  - repo: "gofiber/fiber"
    tool: "govulncheck"
    command: "govulncheck ./..."
  - repo: "opentofu/opentofu"
    tool: "govulncheck"
    command: "govulncheck -format json ./cmd/tofu"
---
