---
title: Config-Aware Startup Failures
description: 'When adding startup preflight checks (permissions, filesystem writeability,
  required directories), treat failure as part of error-handling policy: be precise,
  actionable, and configuration-aware.'
repository: maximhq/bifrost
label: Error Handling
language: Shell
comments_count: 3
repository_stars: 6862
---

When adding startup preflight checks (permissions, filesystem writeability, required directories), treat failure as part of error-handling policy: be precise, actionable, and configuration-aware.

**Standard**
1. **Fail fast only when truly required.** If the app is configured to use external stores or otherwise won’t write to `APP_DIR`, don’t crash-loop just because the directory is read-only.
2. **Provide an escape hatch for intentional exceptions.** If you perform a writeability probe, allow an explicit override (e.g., `BIFROST_SKIP_WRITE_CHECK=1`) to downgrade `exit 1` to a warning in known-safe scenarios.
3. **Make errors actionable.** When exiting, print what was checked (owned UID:GID, mode) and concrete fixes (own the UID, group-writable for supplemental group like 0, set `podSecurityContext.fsGroup`).
4. **Avoid pathological control flow.** For shell argument parsing/loops, ensure conditions and iteration always make progress (don’t keep `$#` constant while “looping” via `set -- ...; shift`).

**Example pattern (self-contained)**
```sh
APP_DIR=${APP_DIR:-/app/data}
SKIP_WRITE_CHECK=${BIFROST_SKIP_WRITE_CHECK:-0}

app_dir_writable() {
  probe="$APP_DIR/.write-test.$$"
  if [ -e "$probe" ]; then probe="$probe.$(date +%s)"; fi
  mkdir "$probe" 2>/dev/null && rmdir "$probe" 2>/dev/null
}

ensure_app_dir() {
  mkdir -p "$APP_DIR" 2>/dev/null || true
  [ -d "$APP_DIR" ] || { echo "Error: cannot create $APP_DIR"; exit 1; }

  if [ "$SKIP_WRITE_CHECK" = "1" ]; then
    echo "Warning: skipping $APP_DIR write check (BIFROST_SKIP_WRITE_CHECK=1)"
    return 0
  fi

  if ! app_dir_writable; then
    uid=$(id -u); gid=$(id -g)
    data_uid=$(stat -c '%u' "$APP_DIR" 2>/dev/null || echo 0)
    data_gid=$(stat -c '%g' "$APP_DIR" 2>/dev/null || echo 0)

    echo "Error: $APP_DIR not writable by UID:GID $uid:$gid (owned by $data_uid:$data_gid)"
    echo "Fix: make it owned by this UID or group-writable for a supplemental group (e.g., GID 0), or set podSecurityContext.fsGroup"
    exit 1
  fi
}
```

Applying this standard reduces crash-loops, makes failures diagnosable, and prevents “strict checks” from blocking valid deployments where writes are unnecessary.