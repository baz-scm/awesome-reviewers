---
title: "Custom rule packs"
code: "V1007.004"
slug: "custom-rule-packs"
technique: "Static application security testing"
technique_id: "V1007"
technique_slug: "static-application-security-testing"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Rules for the framework and helpers your code uses, with tests for each rule."
repos: 15
craft:
  - "Write a rule for each wrapper that bypasses a safe path, such as a raw query builder or an unchecked HTTP client."
  - "Add a positive and a negative test file per rule and run the rule tests in CI."
  - "Keep each rule beside the code it covers and review rule changes like production code."
reverse:
  - "A rules directory with one YAML file per framework helper."
  - "Test files paired with each rule, with annotations that mark expected findings."
  - "A CI step that runs the rule test command, such as semgrep --test."
packages:
  - id: "semgrep"
    name: "Semgrep CE"
    url: "https://github.com/semgrep/semgrep"
  - id: "opengrep"
    name: "Opengrep"
    url: "https://github.com/opengrep/opengrep"
tools:
  - name: "semgrep"
    repos: 15
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
  - repo: "diegosouzapw/OmniRoute"
    tool: "semgrep"
    command: "semgrep scan --config p/owasp-top-ten --config p/secrets --sarif --output semgrep.sarif --metrics off"
---
