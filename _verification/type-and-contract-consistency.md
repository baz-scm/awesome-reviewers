---
title: "Type and contract consistency"
code: "V1035.003"
slug: "type-and-contract-consistency"
technique: "Logic and correctness review"
technique_id: "V1035"
technique_slug: "logic-and-correctness-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Check that values crossing module boundaries keep their meaning."
repos: 148
craft:
  - "Run the type checker in strict mode across every package in the repository."
  - "Annotate public interfaces and the values that cross module boundaries."
  - "Fail CI on any type error, with no blanket ignore comments at module boundaries."
reverse:
  - "A strict setting in tsconfig.json, mypy or pyright config files."
  - "A CI step that runs tsc --noEmit, mypy or pyright."
  - "Type stubs or declaration files for the public API."
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
