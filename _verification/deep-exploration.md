---
title: "Deep exploration"
code: "V1034.002"
slug: "deep-exploration"
technique: "Agentic exploration"
technique_id: "V1034"
technique_slug: "agentic-exploration"
tactic: "Code review"
tactic_id: "VA06"
description: "Focused sub-agents that investigate one concern each."
repos: 0
craft:
  - "Start one sub-agent per concern from the survey."
  - "Give each sub-agent read, search and run tools for its own concern only."
  - "Merge the sub-agent findings into one list with the evidence for each."
reverse:
  - "A graph or workflow definition that fans out one branch per concern."
  - "Review comments that cite evidence from several files for one finding."
  - "Stored traces of each sub-agent run kept next to its findings."
packages:
  - id: "langgraph"
    name: "LangGraph"
    url: "https://github.com/langchain-ai/langgraph"
tools: []
examples: []
---
