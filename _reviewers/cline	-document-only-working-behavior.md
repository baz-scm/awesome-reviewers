---
title: Document only working behavior
description: Documentation should describe what the product actually does today, not
  what it used to do, what is planned, or what is currently broken or ignored. If
  a feature, flag, or config option has been deprecated, disabled, or no longer has
  any effect, remove it from the docs rather than keeping an entry that says "this
  does nothing" or "accepted but ignored." A...
repository: "cline/cline\t"
label: Documentation
language: Other
comments_count: 4
repository_stars: 70947
---

Documentation should describe what the product actually does today, not what it used to do, what is planned, or what is currently broken or ignored. If a feature, flag, or config option has been deprecated, disabled, or no longer has any effect, remove it from the docs rather than keeping an entry that says "this does nothing" or "accepted but ignored." A row like `CLINE_HOOKS_DIR | Additional hooks directory` left in a table after the feature stopped working is misleading; either fix the underlying behavior and keep the doc, or delete the doc. Documenting a non-functional option invites users to rely on it and makes the docs look inconsistent (why document this broken thing and not others?).

The only exception is a caveat that is actively being fixed: if a feature is temporarily broken but a near-term fix is in progress, it's fine to note the caveat explicitly (e.g., "this currently returns X due to bug #123, fix in progress") so readers know it will change back. Don't use vague "soon to be deprecated" language indefinitely — once a feature is actually removed or neutered, update or delete the doc promptly instead of leaving stale references.

This also applies to tables and reference lists that imply completeness (e.g., a list of all JSON output types or all tool-call providers): don't assert exhaustiveness unless it's true, and give readers practical, actionable guidance for the general case (e.g., "scripts should skip event types they don't recognize" rather than listing every possible status-only line). When removing a row or claim, prefer clarifying actual current behavior (such as sort order or defaults) over leaving an ambiguous or outdated statement.