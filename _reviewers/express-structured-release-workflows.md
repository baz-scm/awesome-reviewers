---
title: Structured release workflows
description: 'Implement a clearly defined release strategy that distinguishes between
  different types of changes. Create separate workflows for patch releases (typo fixes,
  safe dependency updates, low-risk fixes) and non-patch releases (features, breaking
  changes):'
repository: expressjs/express
label: CI/CD
language: Markdown
comments_count: 3
repository_stars: 67300
---

Implement a clearly defined release strategy that distinguishes between different types of changes. Create separate workflows for patch releases (typo fixes, safe dependency updates, low-risk fixes) and non-patch releases (features, breaking changes):

For patch releases:
- Use direct commits to the main branch for simple, low-risk changes
- Verify with appropriate tests before releasing
- Document changes in a consistent format

For non-patch releases:
- Create dedicated feature branches (e.g., `4.13`, `5.0`)
- Track changes through a release pull request that documents all included changes
- Implement proper access controls for release automation
- Consider using shared credentials stored securely for release publishing

Example workflow for non-patch release:
```
# Create a new branch for the release
git checkout -b 5.0

# Make and commit your changes
...

# Open a release PR tracking all changes
# Example: https://github.com/expressjs/express/pull/2682

# After review and approval, merge and publish
npm version minor  # or major for breaking changes
git push origin --tags
npm publish
```

This structured approach ensures changes are properly tracked, reviewed, and deployed according to their risk level, making the release process more predictable and maintainable.