---
title: "Round-trip properties"
code: "V1021.001"
slug: "round-trip-properties"
technique: "Property-based tests"
technique_id: "V1021"
technique_slug: "property-based-tests"
tactic: "Testing"
tactic_id: "VA04"
description: "decode(encode(x)) == x for serializers and parsers."
repos: 23
craft:
  - "Write a property asserting that decoding an encoded value returns the original value."
  - "Generate inputs with the framework's strategies for the value's types."
  - "Keep the property test next to the codec and run it in the normal test job."
reverse:
  - "@given tests that call an encode and a decode function and assert equality."
  - "fc.assert with fc.property calls around serializer or parser functions."
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
