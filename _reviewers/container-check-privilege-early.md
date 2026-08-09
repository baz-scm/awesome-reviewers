---
title: Check Privilege Early
description: When a script performs privileged or security-sensitive actions (e.g.,
  deleting/installing application files in system directories), explicitly enforce
  the required authorization before proceeding.
repository: apple/container
label: Security
language: Shell
comments_count: 1
repository_stars: 48787
---

When a script performs privileged or security-sensitive actions (e.g., deleting/installing application files in system directories), explicitly enforce the required authorization before proceeding.

In shell scripts, gate the privileged logic with an effective-UID check (root/admin), and only show the “admin password required” message when the check fails (typically exit afterward).

```sh
# Example pattern for privileged scripts
if [ "$EUID" -ne 0 ]; then
  echo "This script requires administrator (root) privileges to remove the application files from system directories."
  exit 1
fi

# Privileged operations go here
# rm -rf /system/path/... 
```

This prevents partial execution and reduces security risk by ensuring unauthorized users can’t reach code paths that modify protected locations.