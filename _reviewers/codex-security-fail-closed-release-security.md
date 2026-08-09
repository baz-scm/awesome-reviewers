---
title: Fail-Closed Release Security
description: Any security-sensitive release/publish workflow must be deterministic,
  run only on trusted code, validate against authoritative data, and fail closed.
repository: openai/codex-security
label: Security
language: Yaml
comments_count: 4
repository_stars: 9394
---

Any security-sensitive release/publish workflow must be deterministic, run only on trusted code, validate against authoritative data, and fail closed.

Apply this standard when authoring/changing CI/CD steps that publish artifacts (npm, GitHub releases, containers).

Checklist
- Trusted ref gating + pinned checkout: Only allow publish/backfill logic from protected refs (e.g., main) and pin the checkout/ref used by the security verification steps.
- Strict, authoritative validation: Validate candidate versions/inputs against the source of truth (e.g., npm public history, package.json version, non-empty scan inputs). Use precision-safe numeric semver parsing and reject malformed/empty/unexpected registry responses.
- Provenance/signature verification: Verify signed provenance/attestations and required metadata/schema using a pinned Node/npm toolchain (avoid “latest” implicit changes).
- Immutable promotion records: When promoting/publishing images, verify and record immutable digests and require them before downstream steps.
- Least-privilege job scoping: Split high-risk steps (e.g., provenance signing) into narrowly permissioned jobs rather than granting broad write permissions to the entire workflow.
- Regression coverage: Add tests that run the actual validation/release shell step(s) and cover malformed/unexpected cases.

Example (fail-closed validation pattern)
```bash
set -euo pipefail

# Trusted ref gate (example)
if [[ "${GITHUB_REF}" != "refs/heads/main" ]]; then
  echo "Publish is allowed only from main." >&2
  exit 1
fi

# Strict semver gate (example)
if [[ ! "$CANDIDATE_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Malformed version; refusing to publish." >&2
  exit 1
fi

# Authoritative-source check (example pseudocode)
# - fetch complete stable history
# - parse semver components numerically
# - require candidate > every stable version
# - if history/malformed -> fail closed
if ! validate_candidate_exceeds_all_stable_versions "$CANDIDATE_VERSION"; then
  echo "Version validation failed; refusing to publish." >&2
  exit 1
fi
```

Outcome: developers get a consistent, enforceable process that prevents publishing from untrusted refs, rejects tampered/ambiguous inputs, and verifies what is being released with pinned tooling and cryptographic provenance.