---
title: "Documentation lookup"
code: "V1044.001"
slug: "documentation-lookup"
technique: "External contract verification"
technique_id: "V1044"
technique_slug: "external-contract-verification"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Fetch the exact library version's documentation or source."
repos: 0
craft:
  - "Read the resolved library version from the lockfile."
  - "Fetch the documentation or source for that exact version through the lookup server."
  - "Attach the cited documentation section to each finding that depends on library behaviour."
reverse:
  - "A Context7 MCP server entry in the review configuration."
  - "Lockfile version pins that the review job reads before it queries documentation."
packages:
  - id: "context7"
    name: "Context7"
    url: "https://github.com/upstash/context7"
tools: []
examples: []
---
