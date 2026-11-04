---
title: "Mutation testing"
code: "V1023"
slug: "mutation-testing"
tactic: "Testing"
tactic_id: "VA04"
description: "Changes the code on purpose and checks that some test fails; surviving mutants show tests that do not constrain behaviour."
subtechniques:
  - id: "V1023.001"
    name: "Diff-scoped mutation"
    slug: "diff-scoped-mutation"
    description: "Mutate only lines changed in the PR to keep runtime bounded."
  - id: "V1023.002"
    name: "Mutation score gate"
    slug: "mutation-score-gate"
    description: "Fail when the score on changed code drops below a threshold."
---
