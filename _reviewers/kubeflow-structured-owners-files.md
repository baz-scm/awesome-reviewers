---
title: Structured OWNERS files
description: 'OWNERS files must follow project documentation standards to properly
  reflect component ownership and maintainership. When creating or updating these
  files:'
repository: kubeflow/kubeflow
label: Documentation
language: Other
comments_count: 3
repository_stars: 15064
---

OWNERS files must follow project documentation standards to properly reflect component ownership and maintainership. When creating or updating these files:

1. List approvers who are actively driving the component and have explicitly agreed to participate
2. Do not duplicate people between approver and reviewer sections
3. Leave sections empty if there are no appropriate people to list rather than filling them incorrectly
4. Reference project guidelines for file structure (e.g., Kubeflow documentation standards)

Example of a properly structured OWNERS file:
```yaml
approvers:
  - developer1
  - developer2
  - developer3
reviewers:
  - reviewer1
  - reviewer2
```

If someone should be both an approver and a reviewer, only list them as an approver. This ensures clear documentation of component ownership and streamlines the review process.
