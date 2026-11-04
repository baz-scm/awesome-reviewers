---
title: "Import ordering"
code: "V1001.002"
slug: "import-ordering"
technique: "Formatting"
technique_id: "V1001"
technique_slug: "formatting"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Sort and group imports so they never cause conflicts or noise."
repos: 9
craft:
  - "Enable an import sorter for the language, such as isort or the ruff isort rules."
  - "Set the import groups (standard library, third-party, first-party) in its config."
  - "Run the sorter in the same format step so import changes land in one pass."
reverse:
  - "isort settings in pyproject.toml or setup.cfg, such as profile = \"black\"."
  - "An import-sort rule such as I001 enabled in the linter config."
  - "Import blocks grouped the same way across files in the codebase."
packages:
  - id: "isort"
    name: "isort"
    url: "https://github.com/PyCQA/isort"
tools:
  - name: "isort"
    repos: 9
examples:
  - repo: "django/django"
    tool: "isort"
    command: "pre-commit hook isort"
  - repo: "Aider-AI/aider"
    tool: "isort"
    command: "pre-commit hook isort"
  - repo: "celery/celery"
    tool: "isort"
    command: "pre-commit hook isort"
  - repo: "sgl-project/sglang"
    tool: "isort"
    command: "pre-commit hook isort"
  - repo: "prowler-cloud/prowler"
    tool: "isort"
    command: "pre-commit hook isort"
---
