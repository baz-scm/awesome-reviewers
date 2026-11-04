---
title: "Link checking"
code: "V1010.002"
slug: "link-checking"
technique: "Documentation build"
technique_id: "V1010"
technique_slug: "documentation-build"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Check internal and external links on a schedule."
repos: 0
craft:
  - "Run a link checker over the docs on every pull request for internal links."
  - "Schedule a weekly run that checks external links."
  - "Record exclusions for flaky hosts in the checker config and review them."
reverse:
  - "A lychee configuration file or a lychee step in a CI workflow."
  - "A scheduled workflow with a cron trigger that runs the link checker."
packages:
  - id: "lychee"
    name: "lychee"
    url: "https://github.com/lycheeverse/lychee"
tools: []
examples: []
---
