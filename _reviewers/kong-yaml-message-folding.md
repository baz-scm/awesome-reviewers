---
title: YAML Message Folding
description: When writing YAML string fields intended for one-line or sentence-like
  messages, prefer folded block scalars (`>`) so embedded newlines render as spaces.
  Use literal block scalars (`|`) only when you explicitly need to preserve line breaks.
repository: Kong/kong
label: Code Style
language: Yaml
comments_count: 2
repository_stars: 43871
---

When writing YAML string fields intended for one-line or sentence-like messages, prefer folded block scalars (`>`) so embedded newlines render as spaces. Use literal block scalars (`|`) only when you explicitly need to preserve line breaks.

Example:
```yaml
# Fold newlines into spaces (recommended for sentence-style messages)
message: >
  Fix TCP error
  with updated restriction handling

# Preserve line breaks exactly
message: |
  Fix TCP error
  with updated restriction handling
```

If you see changelog entries using `|` where the message should read as a single paragraph, switch to `>` to match the intended formatting.