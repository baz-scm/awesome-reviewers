---
title: "Convention and guideline review"
id: "V1036"
slug: "convention-and-guideline-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Checks a change against the repository's written rules: style guides, AGENTS.md, architecture decisions, naming conventions."
subtechniques:
  - id: "V1036.001"
    name: "Rule file review"
    description: "Apply the rules in AGENTS.md, CLAUDE.md or CONTRIBUTING.md to the diff."
  - id: "V1036.002"
    name: "Naming and conciseness"
    description: "Flag unclear names, typos and needless code."
  - id: "V1036.003"
    name: "Rule-to-lint promotion"
    description: "Turn rules that can be matched syntactically into lint or Semgrep rules."
packages:
  - id: "pr-agent"
    name: "PR-Agent"
    url: "https://github.com/The-PR-Agent/pr-agent"
  - id: "semgrep"
    name: "Semgrep CE"
    url: "https://github.com/semgrep/semgrep"
  - id: "typos"
    name: "typos"
    url: "https://github.com/crate-ci/typos"
craft:
  - "Keep rules in the repository in one file per scope."
  - "Promote any rule that a pattern can match into a lint rule."
  - "Leave the rest to a reviewer prompt that quotes the rule it applies."
reverse:
  - "AGENTS.md, CLAUDE.md, .cursor/rules or CONTRIBUTING.md with coding rules."
---
