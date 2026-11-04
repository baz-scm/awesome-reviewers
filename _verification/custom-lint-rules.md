---
title: "Custom lint rules"
code: "V1005.003"
slug: "custom-lint-rules"
technique: "Linting"
technique_id: "V1005"
technique_slug: "linting"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Repository-specific rules written as plugins or pattern rules for mistakes that recur in review."
repos: 117
craft:
  - "Pick a recurring review comment and write the pattern it describes as a rule."
  - "Write the rule as an ESLint plugin rule or a Semgrep pattern stored in the repository."
  - "Add a test file for the rule with a failing example and a passing example."
reverse:
  - "A local ESLint plugin directory or an eslint-plugin-* dependency with custom rules."
  - "A .semgrep.yml file or .semgrep/ directory with rules and matching test fixtures."
packages:
  - id: "eslint"
    name: "ESLint"
    url: "https://github.com/eslint/eslint"
  - id: "semgrep"
    name: "Semgrep CE"
    url: "https://github.com/semgrep/semgrep"
tools:
  - name: "eslint"
    repos: 107
  - name: "semgrep"
    repos: 15
examples:
  - repo: "freeCodeCamp/freeCodeCamp"
    tool: "eslint"
    command: "eslint --max-warnings 0"
  - repo: "nousresearch/hermes-agent"
    tool: "eslint"
    command: "eslint {staged_files}"
  - repo: "iptv-org/iptv"
    tool: "eslint"
    command: "eslint scripts/**/*.{ts,js} tests/**/*.{ts,js}"
  - repo: "vercel/next.js"
    tool: "eslint"
    command: "eslint --config eslint.cli.config.mjs"
  - repo: "facebook/react-native"
    tool: "eslint"
    command: "eslint --max-warnings 0 ."
---
