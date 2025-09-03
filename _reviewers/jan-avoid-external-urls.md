---
title: Avoid external URLs
description: Links to external repositories or domains in documentation and code can
  create security vulnerabilities through URL hijacking attacks. Malicious actors
  could potentially gain control of external domains and redirect users to harmful
  content or credential harvesting sites.
repository: menloresearch/jan
label: Security
language: Markdown
comments_count: 1
repository_stars: 37620
---

Links to external repositories or domains in documentation and code can create security vulnerabilities through URL hijacking attacks. Malicious actors could potentially gain control of external domains and redirect users to harmful content or credential harvesting sites.

Always use official, internal, or trusted repository URLs instead of external ones. When linking to documentation, resources, or code examples, ensure the URLs point to your organization's official repositories or well-established, trusted sources.

Example of the security risk:
```markdown
<!-- Vulnerable - external repository -->
- <a href="https://github.com/NHPT/jan/blob/dev/README_CN.md">简体中文</a>

<!-- Secure - official repository -->
- <a href="https://github.com/janhq/jan/blob/dev/README_CN.md">简体中文</a>
```

This practice is especially critical in README files, documentation, and any user-facing content where links could be used to redirect users to potentially malicious sites.