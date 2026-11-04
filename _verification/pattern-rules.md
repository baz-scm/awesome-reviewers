---
title: "Pattern rules"
code: "V1007.001"
slug: "pattern-rules"
technique: "Static application security testing"
technique_id: "V1007"
technique_slug: "static-application-security-testing"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Syntax-aware patterns for dangerous calls and configurations (shell=True, yaml.load, disabled TLS verification)."
repos: 19
craft:
  - "Enable a pattern scanner with a community rule pack for the languages in the repository."
  - "Record the findings at adoption as a baseline so only new findings block a change."
  - "Disable a rule that flags an accepted pattern only in the config, with the reason beside it."
reverse:
  - "A .semgrep.yml file or a rules directory with YAML pattern rules."
  - "A bandit run in CI or pre-commit with a config file listing skipped tests."
  - "A workflow step that runs semgrep or opengrep and uploads SARIF."
packages:
  - id: "opengrep"
    name: "Opengrep"
    url: "https://github.com/opengrep/opengrep"
  - id: "semgrep"
    name: "Semgrep CE"
    url: "https://github.com/semgrep/semgrep"
  - id: "bandit"
    name: "Bandit"
    url: "https://github.com/PyCQA/bandit"
tools:
  - name: "semgrep"
    repos: 15
  - name: "bandit"
    repos: 6
examples:
  - repo: "vitejs/vite"
    tool: "semgrep"
    command: "semgrep scan --quiet --sarif --config auto --exclude playground --exclude __tests__ --exclude-rule javascript.lang.security.audit.detect-non-literal-regexp.dete"
  - repo: "mvanhorn/last30days-skill"
    tool: "semgrep"
    command: "semgrep scan --config=p/default"
  - repo: "appwrite/appwrite"
    tool: "semgrep"
    command: "semgrep test .semgrep"
  - repo: "prisma/prisma"
    tool: "semgrep"
    command: "semgrep scan --severity ERROR --error --sarif --config auto --exclude-rule javascript.express.security.express-wkhtml-injection.express-wkhtmltoimage-injection "
  - repo: "apache/airflow"
    tool: "bandit"
    command: "bandit"
---
