---
title: "Thread classification"
code: "V1056.002"
slug: "thread-classification"
technique: "Review comment resolution"
technique_id: "V1056"
technique_slug: "review-comment-resolution"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Classify threads as addressed, disputed, deferred or open."
repos: 0
craft:
  - "Define four labels: addressed, disputed, deferred and open."
  - "Classify each thread from its comments and commits and store the label with a reason."
  - "Post a reply on every thread that is not addressed."
reverse:
  - "A label enum with addressed, disputed, deferred and open values."
  - "A workflow that posts follow-up comments after a push."
  - "Stored classification output with a reason field per thread."
packages:
  - id: "instructor"
    name: "Instructor"
    url: "https://github.com/567-labs/instructor"
tools: []
examples: []
---
