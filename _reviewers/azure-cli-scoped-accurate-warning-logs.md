---
title: Scoped, Accurate Warning Logs
description: 'When adding warnings/logs, treat them as part of the user experience:
  only emit warnings when they are actionable, accurate, and non-noisy—especially
  when runtime feature detection changes behavior.'
repository: Azure/azure-cli
label: Logging
language: Python
comments_count: 7
repository_stars: 4592
---

When adding warnings/logs, treat them as part of the user experience: only emit warnings when they are actionable, accurate, and non-noisy—especially when runtime feature detection changes behavior.

Guidelines:
- Scope warnings to the exact scenario that needs it (don’t warn unconditionally). If a warning only applies under specific preconditions, move it closer to the triggering branch.
- If you use capability/shape guards (e.g., `hasattr` on an SDK operation group) that can silently change behavior, log a warning when the guarded path is unavailable so users can understand why an expected lookup/action didn’t happen.
- Avoid misleading guidance when settings override each other or when the message may not apply; consider existing configuration before warning.
- Ensure warning content is correct and specific (e.g., OS/plan type labels must match Hyper-V vs Windows).
- Prefer emitting large/raw content through the intended CLI rendering path; avoid logging raw payloads redundantly if it will also be displayed.
- For CLI commands, keep informational output off stdout when it could interfere with scripting—write it to stderr.

Example pattern (behavior-guard warning):

```python
if not hasattr(cert_orders_client, 'app_service_certificate_orders'):
    logger.warning(
        "Certificate orders operation group is unavailable in the current SDK. "
        "Falling back to treating certificate name as a raw Key Vault secret name."
    )
    # fallback behavior...
else:
    # normal behavior...
```

Example pattern (emit accurate stderr for informational text):

```python
import sys
print("Starting interactive shell session...", file=sys.stderr)
```