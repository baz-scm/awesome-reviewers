---
title: Enforce Sensitive File Permissions
description: When creating or updating files that persist user-controlled commands/state
  for later execution (hooks, observer/session forwarding, etc.), treat the contents
  as sensitive and enforce least-privilege permissions at install/write time. Verify
  the permissions in an automated install/integration test so regressions are caught
  early.
repository: ogulcancelik/herdr
label: Security
language: Shell
comments_count: 1
repository_stars: 26924
---

When creating or updating files that persist user-controlled commands/state for later execution (hooks, observer/session forwarding, etc.), treat the contents as sensitive and enforce least-privilege permissions at install/write time. Verify the permissions in an automated install/integration test so regressions are caught early.

Implementation checklist:
- Write the sensitive file with mode 0600 (owner read/write only).
- Add an assertion in your install test to confirm the expected mode.
- Optionally include rationale/comments about the trust boundary, but don’t rely on it to replace permission hardening.

Example (shell + test concept):
```sh
# Ensure the persisted hook/observer command file is owner-only
umask 077
# when creating/updating the file:
# e.g., printf '%s' "$command" > "$hook_file"
# then verify
mode=$(stat -c '%a' "$hook_file")
[ "$mode" = '600' ] || { echo "Expected 0600, got $mode" >&2; exit 1; }
```

This prevents unintended disclosure or tampering of sensitive execution instructions via overly-permissive files (e.g., 0644/0666), aligning with security best practices for stored secrets/state.