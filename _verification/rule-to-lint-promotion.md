---
title: "Rule-to-lint promotion"
code: "V1036.003"
slug: "rule-to-lint-promotion"
technique: "Convention and guideline review"
technique_id: "V1036"
technique_slug: "convention-and-guideline-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Turn rules that can be matched syntactically into lint or Semgrep rules."
repos: 117
craft:
  - "Find review rules that a syntactic pattern can match, such as a banned function call."
  - "Write each one as an ESLint rule or a Semgrep rule and enable it in CI."
  - "Keep the prose rule only where no pattern can match it."
reverse:
  - "Semgrep or ESLint rule messages that cite a rule from AGENTS.md or CONTRIBUTING.md."
  - "Lint configuration entries added in the same commit as a guideline change."
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
