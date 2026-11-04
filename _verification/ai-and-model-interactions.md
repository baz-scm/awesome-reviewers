---
title: "AI and model interactions"
code: "V1059.005"
slug: "ai-and-model-interactions"
technique: "Attack surface inventory"
technique_id: "V1059"
technique_slug: "attack-surface-inventory"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Prompts, tools and retrieved content that cross a trust boundary."
repos: 0
craft:
  - "List each prompt template, tool definition and retrieval source the application uses."
  - "Mark user input and retrieved documents as crossing a trust boundary before they reach the AI service."
  - "Record which tools the AI feature can call and what each tool can access."
reverse:
  - "A threat model entry for the AI service call with untrusted input flagged."
  - "Tool definition files or retrieval configuration that list the sources and tools available to the app."
packages:
  - id: "pytm"
    name: "OWASP pytm"
    url: "https://github.com/OWASP/pytm"
  - id: "threagile"
    name: "Threagile"
    url: "https://github.com/Threagile/threagile"
tools: []
examples: []
---
