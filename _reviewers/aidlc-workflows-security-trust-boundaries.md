---
title: Security Trust Boundaries
description: When software ingests extensions (plugins) or external artifacts (actions/images/deps),
  security standards must explicitly state the trust model and maintenance cadence.
repository: awslabs/aidlc-workflows
label: Security
language: Markdown
comments_count: 2
repository_stars: 3849
---

When software ingests extensions (plugins) or external artifacts (actions/images/deps), security standards must explicitly state the trust model and maintenance cadence.

Apply this rule:
1) **Document trust boundaries where install equals code execution.** If an extension can be composed/loaded from a location without a trust gate (e.g., a “folder-drop” plugin), add a clear security note and user guidance (treat as `git clone && run`; only accept from sources you would run; review the diff; pin to a reviewed tag/release).
2) **Pin supply-chain artifacts, but also define update cadence.** Keep SHA/version pinning for reproducibility and supply-chain safety, and set a cadence per component. Scanner/signature services that intentionally freeze data behind a digest must be updated more frequently (e.g., monthly for ClamAV signature DB digests).
3) **Require verification after updates.** After any pinned update, run the relevant security workflow(s) and confirm outputs (e.g., SARIF uploads/artifacts) and that new findings are expected.

Example language for plugin docs (Kiro folder-drop):
```md
### Security Considerations (Kiro folder-drop)
Kiro plugins are composed on your machine with your shell’s privileges. There is no install-time trust gate—dropping the plugin tree is the trust decision.
Treat a plugin drop like `git clone && run`: only use plugins from sources you would run code from, review the diff, and pin to a reviewed tag/release.
```

Example cadence rule for pinned scanners:
- GitHub Actions / scanner tools: review at least quarterly.
- Signature-backed scanner images (e.g., ClamAV digest): review at least monthly.
- After updating: run the security workflow and validate outputs.