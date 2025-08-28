---
title: Evaluate CI secret exposure
description: Before using secrets in CI/CD workflows that can be triggered by external
  contributors (forks, dependabot), assess the "blast radius" of potential secret
  compromise. Differentiate between high-risk secrets that provide infrastructure
  access and limited-scope secrets with constrained permissions.
repository: kilo-org/kilocode
label: Security
language: Yaml
comments_count: 1
repository_stars: 7302
---

Before using secrets in CI/CD workflows that can be triggered by external contributors (forks, dependabot), assess the "blast radius" of potential secret compromise. Differentiate between high-risk secrets that provide infrastructure access and limited-scope secrets with constrained permissions.

High-risk secrets (avoid in external-triggerable workflows):
- Database passwords, API keys for critical services
- Deployment tokens, infrastructure access keys
- Secrets that allow account modification or data access

Limited-scope secrets (may be acceptable with proper controls):
- Service tokens that only allow specific, non-destructive actions
- Tokens with read-only or upload-only permissions

Example from workflow configuration:
```yaml
# Acceptable: Chromatic token only allows snapshot uploads
- name: Run Chromatic
  uses: chromaui/action@latest
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
```

Always implement additional safeguards like requiring approval for external PR workflows, and document the security tradeoffs when using any secrets in publicly-triggerable workflows.