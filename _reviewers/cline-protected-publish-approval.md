---
title: Protected Publish Approval
description: 'For any CI/CD workflow that publishes or deploys to a protected environment,
  treat the environment-approval gate as an authorization boundary: require human
  maintainer approval for releases/publish actions and never bypass that gate via
  API calls (e.g., `gh api`). Also ensure release artifacts are integrity-checked
  before any publish (e.g., tag must match...'
repository: CLINE/CLINE
label: Security
language: Markdown
comments_count: 1
repository_stars: 70837
---

For any CI/CD workflow that publishes or deploys to a protected environment, treat the environment-approval gate as an authorization boundary: require human maintainer approval for releases/publish actions and never bypass that gate via API calls (e.g., `gh api`). Also ensure release artifacts are integrity-checked before any publish (e.g., tag must match the intended version, and required changelog/release-note structure must be present).

Example policy enforcement (conceptual):
```yaml
# Pseudocode-style: enforce that only an approved deployment can proceed
jobs:
  publish:
    environment: publish  # protected environment requiring manual approval
    steps:
      - name: Validate release identifiers
        run: |
          test "${{ inputs.tag }}" = "v${{ steps.version.outputs.version }}"
      # IMPORTANT: do NOT add any step that approves the environment via API.
      # Never call: gh api ... /environments/.../approvals
      - name: Publish
        run: ./scripts/publish.sh
```

How to apply:
- Mark `publish`/`deploy` targets as protected environments requiring manual approval.
- Require maintainers to approve the run in the UI (“Review deployments”); do not script approvals.
- Add preflight validation for release inputs (version/tag match, required changelog header/structure) so only consistent artifacts can be released after approval.