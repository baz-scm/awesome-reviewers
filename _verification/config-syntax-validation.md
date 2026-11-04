---
title: "Config syntax validation"
code: "V1002.001"
slug: "config-syntax-validation"
technique: "File hygiene"
technique_id: "V1002"
technique_slug: "file-hygiene"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Parse every JSON, YAML and TOML file, and validate the important ones against a schema."
repos: 33
craft:
  - "Add the check-yaml, check-json and check-toml hooks from pre-commit-hooks."
  - "Validate CI workflow and app config files against published JSON schemas with check-jsonschema."
  - "Run the same hooks in CI so a syntax error cannot merge."
reverse:
  - "A .pre-commit-config.yaml that lists check-yaml, check-json or check-toml hook ids."
  - "A check-jsonschema hook or CI step that names a schema file or schema URL for config files."
  - "A CI step that runs pre-commit run --all-files."
packages:
  - id: "pre-commit-hooks"
    name: "pre-commit-hooks"
    url: "https://github.com/pre-commit/pre-commit-hooks"
  - id: "check-jsonschema"
    name: "check-jsonschema"
    url: "https://github.com/python-jsonschema/check-jsonschema"
  - id: "yamllint"
    name: "yamllint"
    url: "https://github.com/adrienverge/yamllint"
tools:
  - name: "pre-commit-hooks"
    repos: 33
examples:
  - repo: "TheAlgorithms/Python"
    tool: "pre-commit-hooks"
    command: "pre-commit hook check-executables-have-shebangs"
  - repo: "langchain-ai/langchain"
    tool: "pre-commit-hooks"
    command: "pre-commit hook check-yaml"
  - repo: "langflow-ai/langflow"
    tool: "pre-commit-hooks"
    command: "pre-commit hook check-case-conflict"
  - repo: "fastapi/fastapi"
    tool: "pre-commit-hooks"
    command: "pre-commit hook check-added-large-files"
  - repo: "ggml-org/llama.cpp"
    tool: "pre-commit-hooks"
    command: "pre-commit hook trailing-whitespace"
---
