---
title: Immutable Setup Pinning
description: 'When your tooling downloads/execut es external installers or scripts,
  treat both the *source* and the *workspace* as security-sensitive:


  - **Pin remote code to an immutable reference** (tag/commit SHA) before executing
  it, so the fetched content can’t change between reviews/runs.'
repository: aaif-goose/goose
label: Security
language: Yaml
comments_count: 2
repository_stars: 51876
---

When your tooling downloads/execut es external installers or scripts, treat both the *source* and the *workspace* as security-sensitive:

- **Pin remote code to an immutable reference** (tag/commit SHA) before executing it, so the fetched content can’t change between reviews/runs.
- **Stage work in a unique temp directory** (e.g., `mktemp -d`) rather than a predictable hardcoded path, so pre-existing/stale files can’t affect the install.

Example (bash):
```bash
set -euo pipefail

# 1) Immutable source pin
REPO_URL="https://github.com/modib/agent-toolkit.git"
PIN="v1.0.0"  # or better: a commit SHA

# 2) Unique workspace
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

git clone "$REPO_URL" "$WORKDIR/herdr-setup"
cd "$WORKDIR/herdr-setup"
git checkout "$PIN"

# Execute installer from the pinned content
bash "goose/plugins/herdr/install.sh"
```

Apply this standard to any build/install/automation steps that clone repos, download scripts, or run them from a working directory.