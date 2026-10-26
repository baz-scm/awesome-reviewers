---
title: Document Real Behavior
description: 'When writing or updating technical docs, ensure users can reliably understand
  what will happen in practice.


  **Standard**

  1. **If a setting/feature has no effect, don’t leave it as normal documentation.**'
repository: cline/cline#v23
label: Documentation
language: Other
comments_count: 2
repository_stars: 70889
---

When writing or updating technical docs, ensure users can reliably understand what will happen in practice.

**Standard**
1. **If a setting/feature has no effect, don’t leave it as normal documentation.**
   - Prefer removing the line from docs, or fixing the product and keeping the doc.
   - Only keep it when you also include a clear caveat (e.g., “has no effect in this release”) and track the remediation.
2. **For non-obvious exceptions, add an attention-getting “Caveats”/“Notes” section.**
   - Explicitly state scope and whether claims are exhaustive.
   - Describe the *class* of cases when you can’t list every provider/tooling scenario.
3. **Prefer actionable guidance over vague warnings.**
   - Tell the user what to do next (e.g., how to verify which hooks/providers are active, what behavior to expect).

**Doc pattern (Markdown)**
```md
## Caveats
> **Important:** `FOO_BAR` has no effect in this release.
> We plan to address this; see issue/PR: #1234.

## Caveats
> **Note:** Some model providers handle tool processing internally, so these hooks may not run.
> The list above is not exhaustive—this applies to providers that execute tool-processing on the provider side.
```

Applying this standard prevents “silly” no-op documentation and reduces user confusion when behavior differs by provider or environment.