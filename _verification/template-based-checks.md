---
title: "Template-based checks"
code: "V1027.002"
slug: "template-based-checks"
technique: "Dynamic security testing"
technique_id: "V1027"
technique_slug: "dynamic-security-testing"
tactic: "Testing"
tactic_id: "VA04"
description: "Targeted requests that confirm a specific vulnerability class."
repos: 0
craft:
  - "Turn each static finding that needs runtime proof into a template."
  - "Store the templates in the repository and run them against the preview environment."
  - "Run only read-only requests against shared environments."
reverse:
  - "A templates directory of YAML files with request and matcher blocks."
  - "A nuclei step in a deployment workflow that passes a template path."
  - "Template IDs referenced from finding records."
packages:
  - id: "nuclei"
    name: "Nuclei"
    url: "https://github.com/projectdiscovery/nuclei"
tools: []
examples: []
---
