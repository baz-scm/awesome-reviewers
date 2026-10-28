---
title: Document actual behavior only
description: Documentation must accurately reflect what the product currently does,
  not what it once did, might do again, or was intended to do. If a feature is broken,
  removed, or has no effect, delete the documentation for it instead of keeping an
  entry with a caveat like "has no effect" or "deprecated soon" — such notes invite
  readers to still try the feature and...
repository: cline/cline#&&sleep 4
label: Documentation
language: Other
comments_count: 6
repository_stars: 70980
---

Documentation must accurately reflect what the product currently does, not what it once did, might do again, or was intended to do. If a feature is broken, removed, or has no effect, delete the documentation for it instead of keeping an entry with a caveat like "has no effect" or "deprecated soon" — such notes invite readers to still try the feature and look out of place next to things that work correctly. Keep a doc entry only if the behavior is real today; if it's a large, in-progress removal, it's fine to note the caveat temporarily, but default to deleting stale or non-functional entries.

This also means every code example, CLI invocation, and table of options/fields in the docs should be verified against actual behavior before merging. For instance, don't document an "accepted but ignored" CLI flag — just remove the row. Order of arguments in examples (e.g., `cline connect telegram --restart -k <TOKEN>` vs. putting the option before the channel) must match what the CLI actually parses, not just what looks reasonable. Field/event tables should only list what's genuinely useful or actionable for the reader, not an exhaustive-but-misleading list that implies completeness.

Finally, use precise verbs that match the real guarantee. Say a system "supports" a control rather than "enforces" it if the control can be bypassed or overwritten by the user — overstating strength misleads readers about what they can rely on.

Example of what to avoid:
```md
| `CLINE_HOOKS_DIR` | Additional hooks directory |
```
when the variable currently has no effect. Either remove the row or fix the underlying bug — don't leave a misleading entry.