---
title: Contract-First Documentation
description: 'All documentation should behave like an interface: precise contracts,
  unambiguous rule precedence, and resilient references.


  Apply this standard by:

  '
repository: bmad-code-org/bmad-method
label: Documentation
language: Markdown
comments_count: 9
repository_stars: 51859
---

All documentation should behave like an interface: precise contracts, unambiguous rule precedence, and resilient references.

Apply this standard by:

1) Define explicit contracts (schemas + invariants)
- When docs describe data exchange, always include the schema and required invariants (e.g., “writing result.json is the LAST action”).
- Specify field meanings and valid values (e.g., per-finding `status`/`severity` enums) and what companion artifacts are produced.

2) Eliminate contradictions via rule precedence
- If there are “auto vs interactive” or “headless vs interactive” branches, document the override order (“these rules override everywhere”) and ensure no section contradicts the stated I/O contract.
- Remove/guard behaviors that violate the contract (e.g., interactive hooks that must not run in automation).

3) Single source of truth; avoid doc duplication that will rot
- Don’t re-embed the same “authoritative contract” knobs across many tutorial/map/docs files.
- Point to the authoritative file (e.g., skill `customize.toml` / `SKILL.md`) instead of duplicating knob-level details.

4) Make references robust to installation/layout
- Use explicit relative paths and keep cross-skill format definitions local (ship your own copy when referencing another skill would cross a boundary).
- Fix broken relative links by validating them in the target doc site context.

5) Keep docs consistent with real fallback/merge behavior
- If a script/resolver has a fallback behavior, the docs must describe the real structural rules (e.g., merge-by-shape rules and array merge keys) rather than “later wins” shortcuts that can silently drop defaults.

Example (path robustness pattern)
- Prefer:
  - `./deferred-work-format.md`
  - `../deferred-work-format.md`
- Over cross-boundary references into another skill’s directory that can break when skills are installed independently.