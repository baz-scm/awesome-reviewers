---
title: "Reply sentiment"
code: "V1069.002"
slug: "reply-sentiment"
technique: "Developer feedback capture"
technique_id: "V1069"
technique_slug: "developer-feedback-capture"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Classify replies as agreeing, disputing or neutral."
repos: 0
craft:
  - "Collect the replies on each bot comment after the pull request closes."
  - "Label each reply as agreeing, disputing or neutral."
  - "Store the label next to the finding's outcome record."
reverse:
  - "A pull_request_review_comment webhook handler that writes replies to a store."
  - "A labelled sample file of replies marked agreeing, disputing or neutral."
packages: []
tools: []
examples: []
---
