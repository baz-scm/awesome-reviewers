---
title: Harden CI/CD workflows
description: Treat GitHub Actions workflows as part of the security attack surface,
  since they can run with repository write access and secrets. When referencing third-party
  actions, pin them to a specific commit SHA rather than a mutable tag (e.g. `v1`)
  to prevent supply-chain attacks if the upstream action is compromised or updated
  maliciously; document how pinned...
repository: expressjs/Express
label: Security
language: Yaml
comments_count: 3
repository_stars: 69579
---

Treat GitHub Actions workflows as part of the security attack surface, since they can run with repository write access and secrets. When referencing third-party actions, pin them to a specific commit SHA rather than a mutable tag (e.g. `v1`) to prevent supply-chain attacks if the upstream action is compromised or updated maliciously; document how pinned hashes will be kept up to date (e.g. via automated PRs). Grant the minimum permissions necessary, using fine-grained tokens scoped only to what the workflow needs, and verify that any action does not inadvertently log secrets (GitHub will redact known secrets, but avoid printing them intentionally). Avoid `pull_request_target` for workflows that check out or execute PR code, since it runs with the base repository's elevated privileges and allows an attacker's PR to execute arbitrary code in that privileged context; prefer `pull_request` instead. If `pull_request_target` is unavoidable (e.g., to post comments or manage labels), do not check out or execute untrusted PR content, and explicitly guard against script injection in any inputs derived from the PR (titles, branch names, file contents, etc.).