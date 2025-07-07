---
title: Implement least privilege
description: 'Apply the principle of least privilege for all repository and system
  access to enhance security. Each role should be granted only the permissions necessary
  to perform their specific responsibilities:'
repository: expressjs/express
label: Security
language: Markdown
comments_count: 3
repository_stars: 67300
---

Apply the principle of least privilege for all repository and system access to enhance security. Each role should be granted only the permissions necessary to perform their specific responsibilities:

1. Repository maintainers should have "maintain access" rather than "admin rights" for day-to-day operations
2. Security reports should follow a dedicated triage process through security teams first
3. Release capabilities should be restricted to authorized individuals with appropriate permissions

This practice reduces the attack surface and limits the potential impact of compromised accounts.

Example implementation in team documentation:
```
# Repository Access Levels

- TC Members: Admin access
- Repository Captains: Maintain access and package publication rights
- Contributors: Write access to specific repositories
- Security Triage Team: Access to security reports

Security vulnerabilities must be reported to the security triage team first, who will involve repository captains after initial assessment.
```