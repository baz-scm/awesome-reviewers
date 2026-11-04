---
title: "Strict mode"
code: "V1006.002"
slug: "strict-mode"
technique: "Type checking"
technique_id: "V1006"
technique_slug: "type-checking"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Disallow implicit any, untyped definitions and unchecked optional access."
repos: 148
craft:
  - "Set strict to true in tsconfig.json, or run mypy and pyright in strict mode."
  - "Enable noImplicitAny and strictNullChecks, or disallow untyped definitions in mypy."
  - "Fix the baseline errors and block new untyped or unchecked code in CI."
reverse:
  - "A tsconfig.json with \"strict\": true in compilerOptions."
  - "A CI step running mypy --strict or a strict pyright configuration."
packages:
  - id: "typescript"
    name: "TypeScript (tsc)"
    url: "https://github.com/microsoft/TypeScript"
  - id: "mypy"
    name: "mypy"
    url: "https://github.com/python/mypy"
  - id: "pyright"
    name: "Pyright"
    url: "https://github.com/microsoft/pyright"
tools:
  - name: "tsc"
    repos: 117
  - name: "mypy"
    repos: 35
  - name: "pyright"
    repos: 16
examples:
  - repo: "freeCodeCamp/freeCodeCamp"
    tool: "tsc"
    command: "tsc -p tsconfig.build.json"
  - repo: "nousresearch/hermes-agent"
    tool: "tsc"
    command: "tsc --noEmit -p tsconfig.json"
  - repo: "microsoft/vscode"
    tool: "tsc"
    command: "tsc --project build/tsconfig.json"
  - repo: "vercel/next.js"
    tool: "tsc"
    command: "tsc"
  - repo: "facebook/react-native"
    tool: "tsc"
    command: "tsc -p packages/react-native/__typetests__/tsconfig.legacy.json"
---
