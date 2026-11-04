---
title: "Review comment resolution"
id: "V1056"
slug: "review-comment-resolution"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Checks whether a new commit actually addresses each open review comment before the thread is resolved."
subtechniques:
  - id: "V1056.001"
    name: "Addressed check"
    description: "Compare the comment's request with the code that changed after it."
  - id: "V1056.002"
    name: "Thread classification"
    description: "Classify threads as addressed, disputed, deferred or open."
packages:
  - id: "pygithub"
    name: "PyGithub"
    url: "https://github.com/PyGithub/PyGithub"
  - id: "instructor"
    name: "Instructor"
    url: "https://github.com/567-labs/instructor"
craft:
  - "Fetch open threads and the commits after each."
  - "Ask whether the requested change is present, with the diff hunk as evidence."
  - "Resolve only threads with evidence; reply on the rest."
reverse:
  - "Bots that resolve threads or post follow-ups after pushes."
---
