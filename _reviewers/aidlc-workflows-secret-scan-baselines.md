---
title: Secret scan baselines
description: When using secret-scanning tools (e.g., gitleaks) ignore or baseline
  files, treat those artifacts as sensitive because they may contain previously detected
  secret text.
repository: awslabs/aidlc-workflows
label: Security
language: Other
comments_count: 1
repository_stars: 3849
---

When using secret-scanning tools (e.g., gitleaks) ignore or baseline files, treat those artifacts as sensitive because they may contain previously detected secret text.

Apply this rule:
- Only add ignore/baseline entries when necessary to reduce noise.
- Document what the baseline does (e.g., “detect only new secrets”) and why each ignored path is non-actionable.
- Assume baseline contents are sensitive data (even if they include synthetic/test credentials) and restrict exposure (access control, avoid accidental publication, don’t log contents).

Example (pattern + security note):
```text
# Gitleaks baseline — records pre-existing known findings so gitleaks can
# detect only *new* secrets.
# NOTE: baseline includes matched text from findings (“Secret” and “Match”),
# so treat it as sensitive.
.gitleaks-baseline.json
```