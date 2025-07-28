---
title: Restrict external dependencies
description: Dependencies from packages outside your organization's trusted domain
  pose security risks and should be avoided in pull requests. When package-lock.json
  files include external dependencies, they introduce potential vulnerabilities that
  bypass internal security controls.
repository: cline/cline
label: Security
language: Json
comments_count: 1
repository_stars: 48299
---

Dependencies from packages outside your organization's trusted domain pose security risks and should be avoided in pull requests. When package-lock.json files include external dependencies, they introduce potential vulnerabilities that bypass internal security controls.

Only include dependencies from your organization's approved domains (e.g., internal packages, trusted vendors like AWS in this case). If external dependencies are necessary, they should be reviewed and added through internal security processes rather than directly in pull requests.

When submitting PRs:
- Remove package-lock.json files that reference external domains
- Let security teams handle dependency updates internally
- Focus PR changes on application code rather than dependency management

This approach ensures all external dependencies undergo proper security vetting before being introduced to the codebase.