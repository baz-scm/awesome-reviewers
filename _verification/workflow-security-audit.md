---
title: "Workflow security audit"
code: "V1009.002"
slug: "workflow-security-audit"
technique: "CI workflow linting"
technique_id: "V1009"
technique_slug: "ci-workflow-linting"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Flag template injection, pull_request_target misuse, unpinned third-party actions and write-all permissions."
repos: 33
craft:
  - "Run zizmor over .github/workflows in CI."
  - "Move untrusted ${{ github.event... }} values into environment variables before they reach run: steps."
  - "Pin third-party actions to full commit SHAs and set permissions per job."
reverse:
  - "A zizmor step in a workflow or a zizmor configuration file in the repository."
  - "Third-party uses: lines pinned to 40-character commit SHAs."
packages:
  - id: "zizmor"
    name: "zizmor"
    url: "https://github.com/zizmorcore/zizmor"
tools:
  - name: "zizmor"
    repos: 33
examples:
  - repo: "axios/axios"
    tool: "zizmor"
    command: "uses zizmorcore/zizmor-action"
  - repo: "neovim/neovim"
    tool: "zizmor"
    command: "uses zizmorcore/zizmor-action"
  - repo: "fastapi/fastapi"
    tool: "zizmor"
    command: "zizmor ."
  - repo: "django/django"
    tool: "zizmor"
    command: "uses zizmorcore/zizmor-action"
  - repo: "home-assistant/core"
    tool: "zizmor"
    command: "pre-commit hook zizmor"
---
