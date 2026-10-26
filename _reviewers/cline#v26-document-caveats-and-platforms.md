---
title: Document Caveats and Platforms
description: 'When writing technical documentation, treat user-facing behavior as
  a contract: (1) explicitly document exceptions/caveats for when features don’t apply,
  and (2) include platform-specific details (especially Windows) wherever paths/commands
  differ. Also ensure option tables/examples match actual behavior—avoid phrasing
  that implies an option works if it’s...'
repository: cline/cline#v26
label: Documentation
language: Other
comments_count: 3
repository_stars: 70893
---

When writing technical documentation, treat user-facing behavior as a contract: (1) explicitly document exceptions/caveats for when features don’t apply, and (2) include platform-specific details (especially Windows) wherever paths/commands differ. Also ensure option tables/examples match actual behavior—avoid phrasing that implies an option works if it’s ignored.

Apply this checklist:
- Add a dedicated “Caveats” callout/section for known non-applicability (e.g., “hooks may not run when X happens”).
- Provide concrete platform variants (e.g., show both Unix and Windows path examples instead of relying on `~`).
- For CLI flags and behaviors, only describe what the system actually does; if a behavior is unsupported or never/only sometimes applies, state the condition clearly rather than listing it as a normal option.

Example (doc pattern):

> **Caveats**
> - Hooks run for tool calls made by Cline. If the selected model provider performs tool processing itself, `PreToolUse`/`PostToolUse` may not run.

> **Hooks folders**
> - macOS/Linux: `~/.cline/hooks/`
> - Windows: `%USERPROFILE%\\.cline\\hooks\\` (or the supported equivalent in your product)

> **CLI behavior**
> - If a flag is not honored, don’t include it as a “working” option. Instead, either document the real alternative or clearly state the triggering condition.