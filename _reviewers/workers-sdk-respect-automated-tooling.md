---
title: Respect automated tooling
description: Avoid manually updating files or configurations that are managed by automated
  CI/CD tools. Many modern development workflows rely on automated systems like dependabot
  for dependency updates, changesets for version management, and other tools for consistent
  builds and releases.
repository: cloudflare/workers-sdk
label: CI/CD
language: Json
comments_count: 2
repository_stars: 3379
---

Avoid manually updating files or configurations that are managed by automated CI/CD tools. Many modern development workflows rely on automated systems like dependabot for dependency updates, changesets for version management, and other tools for consistent builds and releases.

Manual interventions can break these automated processes and create inconsistencies across packages or deployments. Instead of manually editing these managed files, use the proper channels provided by the automation tools.

Examples of what to avoid:
- Manually updating dependency versions in package.json when dependabot manages them
- Manually bumping version numbers in package.json when using changesets for release management
- Bypassing established automated workflows for critical CI/CD processes

When you need to make changes that affect automated tooling, first understand how the automation works and whether there's a proper way to achieve your goal through the automated system rather than working around it.