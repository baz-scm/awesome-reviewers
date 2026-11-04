---
title: "Stateful testing"
code: "V1021.003"
slug: "stateful-testing"
technique: "Property-based tests"
technique_id: "V1021"
technique_slug: "property-based-tests"
tactic: "Testing"
tactic_id: "VA04"
description: "Generate sequences of operations and check invariants after each."
repos: 23
craft:
  - "Define the operations the system exposes and the preconditions for each."
  - "Generate random sequences of those operations and run them against the real object."
  - "Check the invariants after every step, not only at the end of a sequence."
reverse:
  - "Classes that subclass RuleBasedStateMachine in Hypothesis test files."
  - "A proptest-state-machine dependency in Cargo.toml with state machine tests."
packages:
  - id: "hypothesis"
    name: "Hypothesis"
    url: "https://github.com/HypothesisWorks/hypothesis"
  - id: "fast-check"
    name: "fast-check"
    url: "https://github.com/dubzzz/fast-check"
  - id: "proptest"
    name: "proptest"
    url: "https://github.com/proptest-rs/proptest"
tools:
  - name: "hypothesis"
    repos: 10
  - name: "fast-check"
    repos: 3
  - name: "proptest"
    repos: 11
examples: []
---
