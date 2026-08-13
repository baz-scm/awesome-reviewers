---
title: Secure CI Invocation
description: 'When updating CI/CD pipeline configuration for third-party tools, apply
  two security rules: (1) never embed secret values directly in command-line arguments;
  (2) pin third-party images/actions to immutable digests to prevent supply-chain
  drift.'
repository: the-pr-agent/pr-agent
label: Security
language: Markdown
comments_count: 2
repository_stars: 12523
---

When updating CI/CD pipeline configuration for third-party tools, apply two security rules: (1) never embed secret values directly in command-line arguments; (2) pin third-party images/actions to immutable digests to prevent supply-chain drift.

1) Secret handling
- Use the CI platform’s variables/secrets so secrets are injected as environment variables.
- Avoid writing secrets into the CLI command where they can appear in logs, process listings, or error output.

Example (Bitbucket-style invocation without inline secrets):
```yaml
pipelines:
  pull-requests:
    '**':
      - step:
          name: PR Agent Review
          image: codiumai/pr-agent:latest
          script:
            - pr-agent --pr_url="https://bitbucket.org/$BITBUCKET_WORKSPACE/$BITBUCKET_REPO_SLUG/pull-requests/$BITBUCKET_PR_ID" review
```
(Assumes required auth values are provided via Bitbucket Variables/Secrets, passed as environment variables by the runner.)

2) Supply-chain pinning
- Pin PR Agent images/actions by digest (not only by tags) for enhanced security.
- Document the digest/SHA (include a digest link) so changes are auditable.

Example (GitHub Actions-style digest pin):
```yaml
- name: PR Agent action step
  id: pragent
  uses: docker://codiumai/pr-agent@sha256:<digest>
# Optional: add a link to the digest page/where the SHA came from
```