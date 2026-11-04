---
title: "Mutation score gate"
code: "V1023.002"
slug: "mutation-score-gate"
technique: "Mutation testing"
technique_id: "V1023"
technique_slug: "mutation-testing"
tactic: "Testing"
tactic_id: "VA04"
description: "Fail when the score on changed code drops below a threshold."
repos: 3
craft:
  - "Set a break threshold on the mutation score for the changed files."
  - "Start the threshold at the current score and raise it in steps."
  - "Fail the job when the score on changed code drops below the threshold."
reverse:
  - "A thresholds block with break and high or low values in the stryker configuration."
  - "A mutationThreshold setting in the pitest build configuration."
packages:
  - id: "stryker"
    name: "StrykerJS"
    url: "https://github.com/stryker-mutator/stryker-js"
  - id: "pitest"
    name: "PIT"
    url: "https://github.com/hcoles/pitest"
tools:
  - name: "stryker"
    repos: 3
examples:
  - repo: "diegosouzapw/OmniRoute"
    tool: "stryker"
    command: "stryker run --config-file stryker.disablebail.json --mutate $BATCH_MUTATE"
---
