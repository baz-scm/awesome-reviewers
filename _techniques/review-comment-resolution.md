---
title: "Review comment resolution"
code: "V1056"
slug: "review-comment-resolution"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Checks whether a new commit actually addresses each open review comment before the thread is resolved."
subtechniques:
  - id: "V1056.001"
    name: "Addressed check"
    slug: "addressed-check"
    description: "Compare the comment's request with the code that changed after it."
  - id: "V1056.002"
    name: "Thread classification"
    slug: "thread-classification"
    description: "Classify threads as addressed, disputed, deferred or open."
---
