---
title: "Per-surface weakness search"
code: "V1060.001"
slug: "per-surface-weakness-search"
technique: "Weakness discovery"
technique_id: "V1060"
technique_slug: "weakness-discovery"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Apply the weakness classes relevant to each surface category."
repos: 0
craft:
  - "List each entry point by surface type, such as HTTP handler, queue consumer or CLI command."
  - "Map each surface type to the weakness classes that apply to it."
  - "Record each weakness with the entry point it can be reached from."
reverse:
  - "A surface inventory file that lists handlers and their surface types."
  - "Security audit reports that cite an entry point for each finding."
  - "Issues labelled security that name a route or handler."
packages:
  - id: "joern"
    name: "Joern"
    url: "https://github.com/joernio/joern"
  - id: "vulnhuntr"
    name: "Vulnhuntr"
    url: "https://github.com/protectai/vulnhuntr"
  - id: "semgrep"
    name: "Semgrep CE"
    url: "https://github.com/semgrep/semgrep"
tools: []
examples: []
---
