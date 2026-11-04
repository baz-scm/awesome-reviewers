---
title: "Unit tests"
code: "V1019.001"
slug: "unit-tests"
technique: "Unit and integration tests"
technique_id: "V1019"
technique_slug: "unit-and-integration-tests"
tactic: "Testing"
tactic_id: "VA04"
description: "Fast, isolated tests per function or class."
repos: 193
craft:
  - "Write one test file per module with cases for each public function or class."
  - "Mock only the external boundaries of each unit under test."
  - "Run the test command in CI on every pull request."
reverse:
  - "tests/ or *_test.* files next to the source they cover."
  - "A test script in package.json, pyproject.toml or a Makefile that runs the runner."
  - "A CI workflow step that runs the test command on pull requests."
packages:
  - id: "pytest"
    name: "pytest"
    url: "https://github.com/pytest-dev/pytest"
  - id: "jest"
    name: "Jest"
    url: "https://github.com/jestjs/jest"
  - id: "vitest"
    name: "Vitest"
    url: "https://github.com/vitest-dev/vitest"
tools:
  - name: "pytest"
    repos: 77
  - name: "jest"
    repos: 38
  - name: "vitest"
    repos: 91
  - name: "unittest"
    repos: 20
  - name: "mocha"
    repos: 10
  - name: "node-test"
    repos: 35
  - name: "go-test"
    repos: 29
  - name: "cargo-test"
    repos: 44
examples:
  - repo: "freeCodeCamp/freeCodeCamp"
    tool: "vitest"
    command: "vitest run"
  - repo: "facebook/react"
    tool: "cargo-test"
    command: "cargo test --workspace"
  - repo: "nousresearch/hermes-agent"
    tool: "pytest"
    command: "pytest ${args[@]}"
  - repo: "TheAlgorithms/Python"
    tool: "pytest"
    command: "pytest --iterations=8 --parallel-threads=auto --ignore-gil-enabled --ignore=computer_vision/flip_augmentation.py --ignore=computer_vision/harris_corner.py --ign"
  - repo: "microsoft/vscode"
    tool: "mocha"
    command: "mocha test/unit/node/index.js --delay --ui=tdd --exit"
---
