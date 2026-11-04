---
title: "Addressed check"
code: "V1056.001"
slug: "addressed-check"
technique: "Review comment resolution"
technique_id: "V1056"
technique_slug: "review-comment-resolution"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Compare the comment's request with the code that changed after it."
repos: 0
craft:
  - "Fetch each open review thread with its diff hunk and the commits made after it."
  - "Ask whether the requested change is present in the code after the hunk."
  - "Resolve a thread only when the evidence cites the changed lines."
reverse:
  - "A script or workflow that calls the pull request review thread API."
  - "Bot comments that link to the commit that addressed a thread."
  - "Thread resolve calls in the automation code."
packages:
  - id: "pygithub"
    name: "PyGithub"
    url: "https://github.com/PyGithub/PyGithub"
  - id: "instructor"
    name: "Instructor"
    url: "https://github.com/567-labs/instructor"
tools: []
examples: []
---
