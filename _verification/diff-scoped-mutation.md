---
title: "Diff-scoped mutation"
code: "V1023.001"
slug: "diff-scoped-mutation"
technique: "Mutation testing"
technique_id: "V1023"
technique_slug: "mutation-testing"
tactic: "Testing"
tactic_id: "VA04"
description: "Mutate only lines changed in the PR to keep runtime bounded."
repos: 4
craft:
  - "Limit the mutation run to lines changed in the pull request using the tool's diff or changed-files option."
  - "Run it on one critical module first to measure runtime."
  - "Run the diff-scoped mutation job as a separate pull request check with a time limit."
reverse:
  - "A stryker or mutmut configuration with paths or incremental mode set."
  - "A CI job that passes a changed-files list or git diff range to the mutation tool."
packages:
  - id: "stryker"
    name: "StrykerJS"
    url: "https://github.com/stryker-mutator/stryker-js"
  - id: "mutmut"
    name: "mutmut"
    url: "https://github.com/boxed/mutmut"
  - id: "cargo-mutants"
    name: "cargo-mutants"
    url: "https://github.com/sourcefrog/cargo-mutants"
  - id: "pitest"
    name: "PIT"
    url: "https://github.com/hcoles/pitest"
tools:
  - name: "stryker"
    repos: 3
  - name: "mutmut"
    repos: 1
examples:
  - repo: "diegosouzapw/OmniRoute"
    tool: "stryker"
    command: "stryker run --config-file stryker.disablebail.json --mutate $BATCH_MUTATE"
  - repo: "BerriAI/litellm"
    tool: "mutmut"
    command: "mutmut run 2>&1"
---
