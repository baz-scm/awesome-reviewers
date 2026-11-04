---
title: "External contract verification"
id: "V1044"
slug: "external-contract-verification"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Checks claims about third-party behaviour (an API can return null, a library throws) against authoritative documentation, and grades how strong that proof is."
subtechniques:
  - id: "V1044.001"
    name: "Documentation lookup"
    description: "Fetch the exact library version's documentation or source."
  - id: "V1044.002"
    name: "Proof grading"
    description: "Grade as definitive (spec or exhaustive enum), illustrative (an example) or unresolved."
packages:
  - id: "context7"
    name: "Context7"
    url: "https://github.com/upstash/context7"
  - id: "searxng"
    name: "SearXNG"
    url: "https://github.com/searxng/searxng"
craft:
  - "Resolve the dependency version from the lockfile."
  - "Fetch that version's docs or source, not the latest."
  - "Keep findings that rest on illustrative proof at lower severity."
reverse:
  - "Documentation MCP servers or doc lookup tools configured for the review agent."
---
