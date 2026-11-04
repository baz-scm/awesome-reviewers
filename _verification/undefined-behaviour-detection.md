---
title: "Undefined-behaviour detection"
id: "V1028"
slug: "undefined-behaviour-detection"
tactic: "Formal"
tactic_id: "VA05"
description: "Executes code under an interpreter or instrumentation that detects memory-safety and aliasing violations."
subtechniques:
  - id: "V1028.001"
    name: "Interpreter-based checking"
    description: "Run tests under an interpreter that tracks every pointer (Miri)."
  - id: "V1028.002"
    name: "Sanitizers"
    description: "Compile with address, thread or undefined-behaviour sanitizers and run the tests."
packages:
  - id: "miri"
    name: "Miri"
    url: "https://github.com/rust-lang/miri"
  - id: "sanitizers"
    name: "Sanitizers (ASan, TSan, UBSan)"
    url: "https://github.com/google/sanitizers"
craft:
  - "Run the unsafe-heavy test subset under the checker in CI."
  - "Add sanitizer builds as separate matrix entries."
  - "Treat every report as a bug; there are no false positives to baseline."
reverse:
  - "cargo miri test or -Zsanitizer flags in workflows."
  - "ASAN_OPTIONS or -fsanitize in build scripts."
---
