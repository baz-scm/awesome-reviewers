---
title: Inherit organization security policies
description: Before implementing custom security documentation or procedures, check
  if your organization already provides standardized security policies that your repository
  can inherit. This avoids duplication, ensures consistency across projects, and leverages
  platform-specific security features. For GitHub repositories, organization-level
  security policies (.github...
repository: spring-projects/spring-boot
label: Security
language: Markdown
comments_count: 1
repository_stars: 77637
---

Before implementing custom security documentation or procedures, check if your organization already provides standardized security policies that your repository can inherit. This avoids duplication, ensures consistency across projects, and leverages platform-specific security features. For GitHub repositories, organization-level security policies (.github repository) are automatically inherited and should be used instead of repository-specific implementations when applicable.

Example:
```markdown
# Instead of creating a repository-specific SECURITY.md file with custom content:
# Reporting a Vulnerability
Please, [open a draft security advisory](https://github.com/org-name/security-advisories/security/advisories/new) if you need to disclose a security issue.

# Simply reference the organization-wide policy:
For reporting security vulnerabilities, please see our [security policy](https://github.com/org-name/repo-name/security/policy).
```