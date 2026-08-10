---
title: Gated deterministic releases
description: All release/publishing workflows must be deterministic, serialized safely,
  and strictly gated so that user-facing artifacts are published only after the release
  candidate has passed the final checks.
repository: openai/codex-security
label: CI/CD
language: Yaml
comments_count: 8
repository_stars: 9394
---
{% raw %}
All release/publishing workflows must be deterministic, serialized safely, and strictly gated so that user-facing artifacts are published only after the release candidate has passed the final checks.

Apply this standard when building CI/CD for npm/GitHub releases, backfills, and container/image promotions:

- Serialize release operations across tags and backfills using a single repository-wide concurrency group with GitHub’s durable queue behavior (so later bumps can’t cancel/replace earlier pending work).
- Validate publish eligibility from event inputs:
  - For tag-triggered publishing, require the exact tag ref (e.g., `refs/tags/...`) and a correct ref type.
  - Require ancestry onto the protected branch (e.g., commit must be on `main`).
- Use a deterministic toolchain in the workflow:
  - Explicitly install the exact required tool version into an isolated temporary prefix.
  - Verify the installed version before continuing.
- Promote only after verification succeeds:
  - Build a release candidate, run verification/attestation checks against that candidate, then publish tags/manifests.
  - Prefer selecting/constructing immutable references by digest first, then attest and run all downstream checks, and only then update `:latest` / version tags.
- Preserve human-authored overrides in automation:
  - If a user manually applied an exclusion label (e.g., `skip-release-notes`), automation must not delete it on subsequent title edits.

Example (pattern for safe promotion ordering):
```yaml
concurrency:
  group: release-${{ github.repository }}
  queue: max

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      # build candidate
      # run integration/verification
      # run attestations as needed
      - name: Verify candidate
        run: |
          set -euo pipefail
          ./scripts/verify-release-candidate.sh

  promote:
    needs: verify
    if: ${{ success() }}
    steps:
      - name: Publish only after success
        run: |
          set -euo pipefail
          # select by digest / candidate reference
          ./scripts/promote-release.sh
```

This prevents out-of-order releases, removes dependency on runner/tool bundling, and avoids scenarios where failures leave user-facing tags published even though verification ultimately failed.
{% endraw %}
