---
title: "Undefined-behaviour detection"
code: "V1028"
slug: "undefined-behaviour-detection"
tactic: "Formal"
tactic_id: "VA05"
description: "Executes code under an interpreter or instrumentation that detects memory-safety and aliasing violations."
subtechniques:
  - id: "V1028.001"
    name: "Interpreter-based checking"
    slug: "interpreter-based-checking"
    description: "Run tests under an interpreter that tracks every pointer (Miri)."
  - id: "V1028.002"
    name: "Sanitizers"
    slug: "sanitizers"
    description: "Compile with address, thread or undefined-behaviour sanitizers and run the tests."
---
