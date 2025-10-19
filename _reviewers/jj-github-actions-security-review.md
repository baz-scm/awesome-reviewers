---
title: GitHub Actions security review
description: 'Always review GitHub Actions workflows for security implications before
  merging, particularly focusing on authentication mechanisms and credential handling.
  Understand what permissions like `id-token: write` grant and their potential attack
  vectors. Ensure secure defaults are explicitly configured, such as disabling credential
  persistence.'
repository: jj-vcs/jj
label: Security
language: Yaml
comments_count: 2
repository_stars: 21171
---

Always review GitHub Actions workflows for security implications before merging, particularly focusing on authentication mechanisms and credential handling. Understand what permissions like `id-token: write` grant and their potential attack vectors. Ensure secure defaults are explicitly configured, such as disabling credential persistence.

Key security considerations:
- Understand JWT token permissions and their scope: "It allows GHA actions to request a JWT token on behalf of your repository"
- Be aware of potential abuse scenarios: "Bad Guys could get a hold of it during an actual execution of this workflow"
- Explicitly disable credential persistence to prevent vulnerabilities: `persist-credentials: false`
- Use security scanning tools to identify configuration issues

When implementing new authentication mechanisms, ensure team members understand the security model and document any special permissions required for maintainer approval.
