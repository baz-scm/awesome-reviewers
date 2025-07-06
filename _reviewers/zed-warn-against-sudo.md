---
title: Warn against sudo
description: Applications that may need elevated privileges should explicitly warn
  against running the entire application with sudo. Instead, implement and document
  proper privilege escalation mechanisms (like polkit on Linux) for specific tasks
  requiring higher permissions.
repository: zed-industries/zed
label: Security
language: Shell
comments_count: 1
repository_stars: 62119
---

Applications that may need elevated privileges should explicitly warn against running the entire application with sudo. Instead, implement and document proper privilege escalation mechanisms (like polkit on Linux) for specific tasks requiring higher permissions.

When your application includes functionality that might tempt users to run it with sudo, provide clear warnings about the security and data integrity risks. Include these warnings in both documentation and relevant UI/CLI interactions.

Example:
```bash
if [[ $EUID -eq 0 ]]; then
    echo "WARNING: Do NOT run this application directly with sudo."
    echo "Doing so may compromise security and make application data unusable."
    echo "See https://example.com/docs/security for proper privilege management."
    exit 1
fi

# For specific elevated tasks, use a dedicated privilege management solution:
setup_elevated_access() {
    if ! command -v pkexec >/dev/null 2>&1; then
        echo "Note: 'pkexec' not detected. You won't be able to edit system files."
        echo "See https://example.com/docs/privileges for more information."
    fi
}
```

This approach isolates privileged operations to specific functions rather than running the entire application with elevated privileges, reducing the security attack surface and preventing potential data corruption.