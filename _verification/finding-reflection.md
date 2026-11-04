---
title: "Finding reflection"
code: "V1050.001"
slug: "finding-reflection"
technique: "Reflection pass"
technique_id: "V1050"
technique_slug: "reflection-pass"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Re-examine each finding against the code and the base-to-head diff."
repos: 0
craft:
  - "Run a second pass that takes each finding, the code and the base-to-head diff."
  - "Use a different prompt and a fresh context for the second pass."
  - "Log the reason each withdrawn finding was withdrawn."
reverse:
  - "A graph definition with a critique node that runs after the finding generation node."
  - "Stored withdrawal reasons on findings that were dropped during review."
packages:
  - id: "langgraph"
    name: "LangGraph"
    url: "https://github.com/langchain-ai/langgraph"
tools: []
examples: []
---
