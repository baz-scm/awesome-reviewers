---
title: "Weakness discovery"
id: "V1060"
slug: "weakness-discovery"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "For each entry point, searches for the weakness classes that apply to it: injection, broken access control, SSRF, deserialization, path traversal."
subtechniques:
  - id: "V1060.001"
    name: "Per-surface weakness search"
    description: "Apply the weakness classes relevant to each surface category."
  - id: "V1060.002"
    name: "Multi-tenancy isolation"
    description: "Check every query and cache key for tenant scoping."
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
craft:
  - "Map each surface category to the weakness classes that apply."
  - "Search with taint queries and an investigating agent."
  - "Record each weakness with the entry point it is reachable from."
reverse:
  - "Security audit reports or issues labelled security."
---
