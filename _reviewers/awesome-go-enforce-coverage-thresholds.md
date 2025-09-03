---
title: Enforce coverage thresholds
description: All code contributions must meet a minimum test coverage threshold of
  80% before being accepted. This ensures adequate testing and helps maintain code
  quality standards across the project.
repository: avelino/awesome-go
label: Testing
language: Markdown
comments_count: 3
repository_stars: 151435
---

All code contributions must meet a minimum test coverage threshold of 80% before being accepted. This ensures adequate testing and helps maintain code quality standards across the project.

When reviewing code or adding new libraries, verify that test coverage meets or exceeds the 80% requirement. Coverage below this threshold should result in a request for additional tests before approval.

Example feedback:
```
Test coverage: 72%, the minimum required coverage is 80%.
```

This standard helps ensure that new code is properly tested and reduces the risk of introducing bugs into the codebase. Teams should configure their CI/CD pipelines to automatically check coverage and fail builds that don't meet this threshold.