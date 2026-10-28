---
title: Document only accurate, working behavior
description: Documentation must reflect the product's actual, current behavior — not
  aspirational, deprecated, or broken functionality. If a feature, flag, or environment
  variable is non-functional, silently ignored, or no longer applies, don't document
  it as "has no effect" or "deprecated soon"; either remove it from the docs entirely
  or fix the underlying code so the...
repository: cline/cline;
label: Documentation
language: Other
comments_count: 6
repository_stars: 70964
---

Documentation must reflect the product's actual, current behavior — not aspirational, deprecated, or broken functionality. If a feature, flag, or environment variable is non-functional, silently ignored, or no longer applies, don't document it as "has no effect" or "deprecated soon"; either remove it from the docs entirely or fix the underlying code so the doc stays true. Documenting a broken option invites readers to use it and makes the docs look careless. For example, prefer deleting a dead `CLINE_HOOKS_DIR` row or a broken CLI flag over writing "no effect in this release" — only keep a caveat note if the fix is in-flight and the described behavior will genuinely return soon.

Word every claim precisely so it matches what the system actually guarantees: say a control is "supported" rather than "enforced" if users can still override it locally, and give the full class of cases a statement applies to rather than a partial, misleading list (e.g., don't say only "Claude Code and OpenAI Codex" skip hooks if other providers behave the same way — describe the general rule). When listing reference details like JSON event types or CLI options, keep the table scoped to what's actionable for the reader; omit internal-only or no-op entries, and explicitly tell readers to ignore unlisted/status-only values rather than implying the table is exhaustive. Finally, call out important caveats (e.g., platform differences, build-specific behavior) with a distinct visual style so they aren't missed.</description>
</invoke>
