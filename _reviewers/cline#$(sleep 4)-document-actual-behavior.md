---
title: Document actual behavior
description: Documentation must accurately reflect what the product currently does,
  not what it used to do, what it's supposed to do, or what a partial list suggests.
  Before merging a doc change, verify the described behavior against the real implementation
  and fix the mismatch rather than papering over it with a caveat.
repository: cline/cline#$(sleep 4)
label: Documentation
language: Other
comments_count: 6
repository_stars: 70978
---

Documentation must accurately reflect what the product currently does, not what it used to do, what it's supposed to do, or what a partial list suggests. Before merging a doc change, verify the described behavior against the real implementation and fix the mismatch rather than papering over it with a caveat.

Specific rules to apply:

1. Don't document broken or non-functional features as if they work. If a config option, flag, or feature has stopped doing anything (e.g. `CLINE_HOOKS_DIR` having "no effect"), either fix the underlying bug or delete the documentation entry. Leaving a line like "Has no effect in this release" invites misuse and raises the question of why it wasn't simply removed.

2. When a feature is deprecated and ineffective (e.g. `.clineignore` no longer being enforced and trivially bypassable), remove its documentation rather than keeping a "deprecated soon" warning indefinitely. Stale deprecation notices are more confusing than no documentation at all.

3. Use precise language that matches the actual guarantee. Avoid words like "enforces" when the real behavior is closer to "supports" or "applies by default but can be overridden." For example, prefer:
   - "Each product supports only the controls marked Yes" 
   over
   - "Each product enforces only the controls marked Yes"
   when users can still edit the underlying files between sessions.

4. Don't imply a reference table or list is exhaustive unless it is. If some values legitimately exist but require no reader action (e.g. internal status events), either omit them explicitly and note that the table isn't exhaustive, or state the omission in the PR/doc so readers comparing against `--help` or source aren't surprised.

5. For caveats about external/variable behavior (e.g. "hooks don't run for tools that the model provider runs itself"), give concrete, actionable guidance and visually distinguish caveats (e.g. a callout/warning style) rather than a buried aside — and avoid implying an incomplete list (e.g. of providers) is complete.

Applying these rules keeps documentation trustworthy: readers should be able to assume that anything described as working, enforced, or exhaustive truly is.