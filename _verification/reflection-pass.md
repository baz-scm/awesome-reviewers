---
title: "Reflection pass"
id: "V1050"
slug: "reflection-pass"
tactic: "Finding validation"
tactic_id: "VA07"
description: "A self-critique step where the reviewer re-reads its own findings with fresh context and keeps, revises or withdraws each."
subtechniques:
  - id: "V1050.001"
    name: "Finding reflection"
    description: "Re-examine each finding against the code and the base-to-head diff."
  - id: "V1050.002"
    name: "Discussion-aware reflection"
    description: "Include existing review threads so the reviewer does not repeat or contradict them."
packages:
  - id: "langgraph"
    name: "LangGraph"
    url: "https://github.com/langchain-ai/langgraph"
  - id: "dspy"
    name: "DSPy"
    url: "https://github.com/stanfordnlp/dspy"
craft:
  - "Run reflection with a different prompt and, ideally, a different model than the reviewer."
  - "Pass the code, not the reviewer's reasoning."
  - "Record why each withdrawn finding was withdrawn."
reverse:
  - "Multi-step review agent graphs with a critique node."
---
