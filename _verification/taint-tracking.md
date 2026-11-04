---
title: "Taint tracking"
code: "V1007.002"
slug: "taint-tracking"
technique: "Static application security testing"
technique_id: "V1007"
technique_slug: "static-application-security-testing"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Follow untrusted input from sources to sinks across functions and files."
repos: 63
craft:
  - "List the untrusted sources (request parameters, uploaded files, environment) and the sinks (SQL, shell, file paths, HTML)."
  - "Enable the dataflow query suite for each language, or write a query for each source-sink pair that is missing."
  - "Run the queries on every pull request and keep the results in code scanning."
reverse:
  - "A codeql-analysis workflow that runs a security query suite."
  - "Custom CodeQL query files (.ql) or a qlpack in the repository."
  - "SARIF uploads from the CodeQL step to code scanning."
packages:
  - id: "joern"
    name: "Joern"
    url: "https://github.com/joernio/joern"
  - id: "semgrep"
    name: "Semgrep CE"
    url: "https://github.com/semgrep/semgrep"
  - id: "opengrep"
    name: "Opengrep"
    url: "https://github.com/opengrep/opengrep"
tools:
  - name: "codeql"
    repos: 63
examples:
  - repo: "microsoft/vscode"
    tool: "codeql"
    command: "uses github/codeql-action/analyze"
  - repo: "nodejs/node"
    tool: "codeql"
    command: "uses github/codeql-action/analyze"
  - repo: "langflow-ai/langflow"
    tool: "codeql"
    command: "uses github/codeql-action/analyze"
  - repo: "microsoft/typescript"
    tool: "codeql"
    command: "uses github/codeql-action/analyze"
  - repo: "mui/material-ui"
    tool: "codeql"
    command: "uses github/codeql-action/analyze"
---
