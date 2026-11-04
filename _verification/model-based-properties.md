---
title: "Model-based properties"
code: "V1021.002"
slug: "model-based-properties"
technique: "Property-based tests"
technique_id: "V1021"
technique_slug: "property-based-tests"
tactic: "Testing"
tactic_id: "VA04"
description: "Compare the implementation against a simple reference model."
repos: 23
craft:
  - "Write a simple, obviously correct version of the function to compare against."
  - "Generate random inputs and assert that the real and simple versions return equal results."
  - "Keep the simple version in the test tree, not in production code."
reverse:
  - "Test files that define a naive version of a function and compare it with the real one under random inputs."
  - "fast-check tests built with fc.commands."
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
