---
title: "Gradual typing"
code: "V1006.001"
slug: "gradual-typing"
technique: "Type checking"
technique_id: "V1006"
technique_slug: "type-checking"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Type-check annotated code first and tighten strictness per module."
repos: 44
craft:
  - "Enable type checking for the modules that already have annotations."
  - "Set per-module strictness, such as [[tool.mypy.overrides]] or per-file pyright strict comments."
  - "Raise strictness for each module once it is annotated and record the list in config."
reverse:
  - "A [tool.mypy] section with overrides for selected modules in pyproject.toml."
  - "A pyright configuration or '# pyright: strict' comments in some source files."
packages:
  - id: "mypy"
    name: "mypy"
    url: "https://github.com/python/mypy"
  - id: "pyright"
    name: "Pyright"
    url: "https://github.com/microsoft/pyright"
tools:
  - name: "mypy"
    repos: 35
  - name: "pyright"
    repos: 16
examples:
  - repo: "langflow-ai/langflow"
    tool: "mypy"
    command: "mypy --namespace-packages -p langflow"
  - repo: "fastapi/fastapi"
    tool: "mypy"
    command: "mypy fastapi"
  - repo: "home-assistant/core"
    tool: "mypy"
    command: "mypy --num-workers=4 homeassistant packages/pylint-home-assistant"
  - repo: "python/cpython"
    tool: "mypy"
    command: "mypy --num-workers 4 --config-file $EXPR/mypy.ini"
  - repo: "pallets/flask"
    tool: "mypy"
    command: "mypy"
---
