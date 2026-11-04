---
title: "Verified code"
code: "V1030.002"
slug: "verified-code"
technique: "Proofs and specifications"
technique_id: "V1030"
technique_slug: "proofs-and-specifications"
tactic: "Formal"
tactic_id: "VA05"
description: "Write code with pre- and post-conditions that a verifier proves (Dafny, Lean, Rocq)."
repos: 3
craft:
  - "Annotate the critical functions with preconditions and postconditions in the verifier's language."
  - "Run the verifier on the proof files in CI and fail on any unproven obligation."
  - "Keep the verified module behind a clear interface so unverified callers stay outside it."
reverse:
  - "*.dfy, *.lean or *.v files in a directory separate from unverified code."
  - "A CI job that runs dafny verify, lake build or coqc on the proof files."
  - "A lakefile or _CoqProject file at the repository root."
packages:
  - id: "dafny"
    name: "Dafny"
    url: "https://github.com/dafny-lang/dafny"
  - id: "lean"
    name: "Lean 4"
    url: "https://github.com/leanprover/lean4"
  - id: "rocq"
    name: "Rocq (Coq)"
    url: "https://github.com/rocq-prover/rocq"
tools:
  - name: "coq"
    repos: 2
  - name: "lean"
    repos: 1
examples: []
---
