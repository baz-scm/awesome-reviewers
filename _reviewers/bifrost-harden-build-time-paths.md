---
title: Harden build-time paths
description: When Dockerfile (or build scripts) use build-args/variables to choose
  target directories for `chown`/`chmod`, validate those paths at build time and fail
  if they target sensitive directories. This prevents overly-permissive ownership
  (e.g., group 0 write access) from becoming reachable via undocumented/override knobs.
repository: maximhq/bifrost
label: Security
language: Dockerfile
comments_count: 1
repository_stars: 6862
---

When Dockerfile (or build scripts) use build-args/variables to choose target directories for `chown`/`chmod`, validate those paths at build time and fail if they target sensitive directories. This prevents overly-permissive ownership (e.g., group 0 write access) from becoming reachable via undocumented/override knobs.

Apply this rule by adding a guard or assertion before any recursive ownership/permission changes. For example:

```dockerfile
ARG APP_DIR=/app/data

# Fail build if a dangerous directory is selected (adjust allowlist/prefix as needed)
RUN case "$APP_DIR" in \
  /app|/app/*) echo "Refusing insecure APP_DIR=$APP_DIR" >&2; exit 1 ;; \
esac

RUN chown -R appuser:0 "$APP_DIR" && chmod -R g=rwX "$APP_DIR"
```

Also prefer explicit allowlists (or “path must start with /app/data”) over implicit assumptions about defaults; don’t rely on the variable being “theoretical” or undocumented to avoid security regressions.