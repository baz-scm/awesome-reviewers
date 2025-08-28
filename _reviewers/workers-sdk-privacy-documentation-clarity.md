---
title: Privacy documentation clarity
description: When documenting data collection practices, telemetry, or analytics features,
  explicitly enumerate what sensitive information is NOT collected to ensure transparency
  and build user trust. Privacy statements should be clear, comprehensive, and easily
  understandable.
repository: cloudflare/workers-sdk
label: Security
language: Markdown
comments_count: 1
repository_stars: 3379
---

When documenting data collection practices, telemetry, or analytics features, explicitly enumerate what sensitive information is NOT collected to ensure transparency and build user trust. Privacy statements should be clear, comprehensive, and easily understandable.

The documentation should specifically list categories of sensitive data that are excluded from collection, such as usernames, raw error logs, stack traces, file paths, file contents, and environment variables. This transparency is crucial for security compliance and user confidence.

Example from telemetry documentation:
```markdown
## What happens with sensitive data?

Cloudflare takes your privacy seriously and does not collect any sensitive information including: usernames, raw error logs, stack traces, file names/paths, content of files, and environment variables. Data is never shared with third parties.
```

This approach helps users understand exactly what privacy protections are in place and demonstrates a commitment to responsible data handling practices.