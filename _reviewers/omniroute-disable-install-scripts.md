---
title: Disable install scripts
description: In security-sensitive build environments (e.g., Docker/CI), prevent dependency
  install/postinstall hooks from executing arbitrary code. Use `npm ci` with `--ignore-scripts`
  to reduce supply-chain risk, but explicitly rebuild and validate any known native/runtime
  dependency that truly must compile/bind for the target platform.
repository: diegosouzapw/OmniRoute
label: Security
language: Dockerfile
comments_count: 1
repository_stars: 33162
---

In security-sensitive build environments (e.g., Docker/CI), prevent dependency install/postinstall hooks from executing arbitrary code. Use `npm ci` with `--ignore-scripts` to reduce supply-chain risk, but explicitly rebuild and validate any known native/runtime dependency that truly must compile/bind for the target platform.

Example (pattern):

```dockerfile
# Require reproducible installs
RUN test -f package-lock.json \
  || (echo "package-lock.json is required" >&2 && exit 1)

# Block broad dependency script execution
RUN npm ci --no-audit --no-fund --legacy-peer-deps --ignore-scripts \
  && npm rebuild better-sqlite3 \
  && node -e "require('better-sqlite3')(':memory:').close()"
```

Apply this standard by:
- Defaulting to `--ignore-scripts` for `npm ci` in container builds.
- Adding narrow, explicit rebuild steps for only the dependencies that require native bindings for the target platform.
- Running a minimal smoke test that loads/uses the rebuilt module to fail fast if the native binding isn’t valid.