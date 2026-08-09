---
title: Validate persisted selections
description: When accepting previously recorded state (digests, coverage manifests,
  etc.), revalidate it against the current computed/authoritative data before proceeding.
  If the value no longer matches, fail fast with a message that tells the user exactly
  what to do next. If you tighten validation rules, preserve backward compatibility
  by versioning the stricter...
repository: openai/codex-security
label: Error Handling
language: Python
comments_count: 2
repository_stars: 9394
---

When accepting previously recorded state (digests, coverage manifests, etc.), revalidate it against the current computed/authoritative data before proceeding. If the value no longer matches, fail fast with a message that tells the user exactly what to do next. If you tighten validation rules, preserve backward compatibility by versioning the stricter behavior (or adding legacy/empty allowances) so older artifacts aren’t rendered unusable.

Example (digest revalidation with clear failure):
```python
def require_committed_diff_digest(target, base, head, content_digest=None):
    current = committed_diff_content_digest(target, base, head)
    if content_digest and content_digest != current:
        raise SystemExit(
            "The committed changes selected for review no longer produce the same "
            "diff. Select the changes to review again."
        )
    return current
```

Example (compatibility-aware validation):
- If a future rule rejects empty/all-inapplicable coverage, gate it behind a version or explicit “authoritative empty inventory” signal; otherwise keep legacy scans readable so valid historical outputs don’t fail during recovery or re-ingestion.