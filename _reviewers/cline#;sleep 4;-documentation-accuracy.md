---
title: Documentation accuracy
description: 'Documentation must describe exactly what the product currently does
  — no more, no less. Before merging doc changes, verify that every claim and example
  is actually true and reproducible against the current build:'
repository: cline/cline#;sleep 4;
label: Documentation
language: Other
comments_count: 5
repository_stars: 70976
---

Documentation must describe exactly what the product currently does — no more, no less. Before merging doc changes, verify that every claim and example is actually true and reproducible against the current build:

- If a feature is deprecated, broken, or no longer takes effect (e.g., a flag that "has no effect in this release"), either fix the underlying product or remove the documentation for it rather than describing non-functional behavior. Don't leave stale docs for things that do nothing — it signals inconsistent standards and misleads users. If removal isn't feasible yet, explicitly call out the caveat with a plan/issue link, but prefer fixing or deleting over indefinitely documenting broken functionality.
- Test command examples exactly as written. A documented example like `cline connect telegram --restart -k <BOT-TOKEN>` must actually work; if argument order or parsing causes it to silently fail, fix the example (and ideally the underlying parsing) rather than publishing something that looks correct but isn't.
- Avoid absolute claims ("lists every line type", "enforces this control") unless they are strictly true. Prefer precise, defensible wording (e.g., "supports" instead of "enforces" when the control can be overridden) and instruct readers how to handle cases not explicitly covered (e.g., "scripts should skip event types they don't recognize") instead of implying exhaustive completeness.
- When a reference table or list is meant to be authoritative, only include entries that are relevant and actionable for the reader; omit internal/status-only items that add noise without value.

In short: treat documentation as a contract with the user — audit it against real behavior, fix or remove inaccurate sections, and phrase claims conservatively so they remain true as the system evolves.