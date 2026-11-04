---
title: "Side-by-side comparison"
code: "V1067.003"
slug: "side-by-side-comparison"
technique: "Reviewer evaluation"
technique_id: "V1067"
technique_slug: "reviewer-evaluation"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Run two reviewer versions on the same set and compare."
repos: 0
craft:
  - "Run two reviewer versions on the same set of labelled changes."
  - "Store each version's findings side by side in one results file."
  - "Merge a reviewer change only when the new version is not worse on recall or precision."
reverse:
  - "A comparison config that names two reviewer versions."
  - "A results report that shows both versions for each case."
  - "A pull request template item that asks for a comparison run on reviewer changes."
packages:
  - id: "promptfoo"
    name: "promptfoo"
    url: "https://github.com/promptfoo/promptfoo"
tools: []
examples: []
---
