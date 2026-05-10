---
title: Precise CI Workflows
description: 'CI workflows should be precise, minimal, and predictable:


  - Trigger only when needed: narrow `on: pull_request.paths` (avoid overly broad
  selectors like `**/*.js` unless required). If the PR doesn’t touch dependency inputs,
  the lockfile validation workflow shouldn’t run.'
repository: mermaid-js/mermaid
label: CI/CD
language: Yaml
comments_count: 5
repository_stars: 87952
---

CI workflows should be precise, minimal, and predictable:

- Trigger only when needed: narrow `on: pull_request.paths` (avoid overly broad selectors like `**/*.js` unless required). If the PR doesn’t touch dependency inputs, the lockfile validation workflow shouldn’t run.
- Avoid unnecessary lockfile diffs: don’t update/recommit `pnpm-lock.yaml` unless the PR actually changes what would require regeneration; this reduces merge-conflict risk.
- Keep workflows DRY/organized: prefer integrating checks (e.g., Shellcheck) into existing shared lint workflows. When moving jobs/steps, ensure `permissions` are set at the correct (job) level.
- Harden scheduled runs: use a cron offset rather than exact hour boundaries to reduce delay/drop risk.
- Use stable bot identity for automated commits: for commits created by scheduled/automation runs, set `author_name`/`author_email` to the GitHub Actions bot identity.

Example trigger narrowing:
```yml
on:
  pull_request:
    paths:
      - 'pnpm-lock.yaml'
      - '**/package.json'
# Avoid adding broad patterns like '**/*.js' unless lockfile validation is truly needed for those changes.
```