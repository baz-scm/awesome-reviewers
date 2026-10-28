---
title: Verify documented behavior accuracy
description: Documentation must describe the product as it actually behaves today,
  not as it once behaved, is assumed to behave, or is planned to behave. Before writing
  or approving a doc change, verify the claim against the real implementation (read
  the source, run the command, or inspect logs/processes) rather than trusting prior
  docs or assumptions. For example,...
repository: 'cline/cline

  '
label: Documentation
language: Other
comments_count: 8
repository_stars: 70942
---

Documentation must describe the product as it actually behaves today, not as it once behaved, is assumed to behave, or is planned to behave. Before writing or approving a doc change, verify the claim against the real implementation (read the source, run the command, or inspect logs/processes) rather than trusting prior docs or assumptions. For example, confirming via `lsof` which process actually writes a given log file caught a page that attributed `cline-core-service.log` to the wrong client, and testing `cline auth` / `cline history --limit` behavior ensured the documented flag semantics matched reality.

When a documented feature, flag, or environment variable is deprecated, broken, or has no effect (e.g., `CLINE_HOOKS_DIR` doing nothing, `.clineignore` no longer being enforced), don't leave it documented as if it still works or as a vague "currently broken" caveat — either fix the underlying behavior to match the docs, or remove the documentation/row entirely. Documenting a non-functional option invites users to rely on it and signals it may return to normal, which is misleading if there's no active plan to fix it.

When documenting conditional or edge-case behavior (e.g., which model providers run tools themselves and thus skip certain hooks, or which build/settings key applies to Nightly vs. stable), be exhaustive and explicit rather than giving a partial example, and double check derived values (like settings keys) against the code that generates them. If a list or table claims completeness (e.g., "every line type"), ensure it truly is complete, or explicitly scope the claim and tell readers how to handle unlisted cases.