---
title: Restrict sensitive file permissions
description: Any file written to disk that stores sensitive or executable content
  (commands, tokens, credentials, hook definitions, etc.) must be created with restrictive
  permissions (e.g., mode 0600) rather than relying on the parent directory's ownership
  or trust boundary alone. Explicitly set the mode when the file is created/written,
  and add an automated test or...
repository: ogulcancelik/herdr#canary966c66ad
label: Security
language: Shell
comments_count: 1
repository_stars: 46332
---

Any file written to disk that stores sensitive or executable content (commands, tokens, credentials, hook definitions, etc.) must be created with restrictive permissions (e.g., mode 0600) rather than relying on the parent directory's ownership or trust boundary alone. Explicitly set the mode when the file is created/written, and add an automated test or assertion that verifies the resulting permissions, so regressions are caught early. For example, when saving a previous hook command to disk before overwriting it:

```python
import os

path = "/home/user/.jcode/hooks/herdr-session-start.previous"
with open(path, "w", encoding="utf-8") as f:
    f.write(command)
os.chmod(path, 0o600)  # restrict to owner read/write only
```

and in the corresponding install/unit test, assert the file mode equals `0o600` to guarantee the restriction is enforced going forward.