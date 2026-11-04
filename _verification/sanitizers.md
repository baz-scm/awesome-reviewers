---
title: "Sanitizers"
code: "V1028.002"
slug: "sanitizers"
technique: "Undefined-behaviour detection"
technique_id: "V1028"
technique_slug: "undefined-behaviour-detection"
tactic: "Formal"
tactic_id: "VA05"
description: "Compile with address, thread or undefined-behaviour sanitizers and run the tests."
repos: 0
craft:
  - "Build the tests with -fsanitize=address, thread or undefined as separate CI matrix entries."
  - "Set ASAN_OPTIONS and UBSAN_OPTIONS so that a report fails the test run."
  - "Run the sanitizer builds on each pull request or on a nightly schedule."
reverse:
  - "A sanitizer matrix in a CI workflow with sanitizer names as values."
  - "-fsanitize flags or RUSTFLAGS with -Zsanitizer in build scripts or CI environment."
packages:
  - id: "sanitizers"
    name: "Sanitizers (ASan, TSan, UBSan)"
    url: "https://github.com/google/sanitizers"
tools: []
examples: []
---
