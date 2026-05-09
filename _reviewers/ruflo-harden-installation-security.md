---
title: Harden installation security
description: Any install/setup instructions and scripts must avoid common supply-chain
  and remote execution risks, and must clearly communicate the security posture.
repository: ruvnet/ruflo
label: Security
language: Other
comments_count: 1
repository_stars: 47002
---

Any install/setup instructions and scripts must avoid common supply-chain and remote execution risks, and must clearly communicate the security posture.

Apply these rules:
- Avoid mutable dependency/version references (e.g., do not use `@latest` for critical packages). Prefer pinned versions.
- Avoid remote script execution as a default installation path (e.g., avoid `curl | bash`). If you must support it, require explicit opt-in and add a user-visible warning.
- Provide a security notice/documentation (e.g., `SECURITY.md` and clear README guidance) that names the risks (supply chain, persistence) and states the safer install direction.
- When code must be fetched/executed during setup, add a “review-before-run” step in the workflow (e.g., print the exact command/script or require inspection prior to execution).

Example (safer install guidance):
```bash
# BAD: remote execution default
curl -fsSL https://example.com/install.sh | bash

# BETTER: pinned artifact + explicit execution step
# (Version is pinned; fetching is logged and execution is explicit)
VERSION='1.2.3'
curl -fsSL -o tool.tgz "https://example.com/tool-${VERSION}.tgz"
# verify checksum/signature here, then extract/run explicitly

tar -xzf tool.tgz
./tool --help
```

Result: fewer opportunities for compromised dependencies or tampered install scripts to affect users, plus clearer expectations for safe setup.