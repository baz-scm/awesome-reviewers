---
title: "Change summary"
code: "V1032.001"
slug: "change-summary"
technique: "Change intent extraction"
technique_id: "V1032"
technique_slug: "change-intent-extraction"
tactic: "Code review"
tactic_id: "VA06"
description: "Generate a description and per-file walkthrough of the diff."
repos: 0
craft:
  - "Pass the pull request title, body and commit messages to the summary generator."
  - "Ask for a per-file walkthrough in the generated description."
  - "Write the output into the pull request body under a fixed heading."
reverse:
  - "A .pr_agent.toml configuration file in the repository."
  - "A generated summary section with a fixed heading in pull request bodies."
packages:
  - id: "pr-agent"
    name: "PR-Agent"
    url: "https://github.com/The-PR-Agent/pr-agent"
tools: []
examples: []
---
