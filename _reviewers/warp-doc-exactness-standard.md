---
title: Doc exactness standard
description: 'Adopt a “docs must be executable-accurate” standard: treat technical
  docs/specs/changelogs as part of the product contract, and ensure they exactly match
  current behavior, supported formats, and rendering constraints.'
repository: warpdotdev/warp
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 56893
---

Adopt a “docs must be executable-accurate” standard: treat technical docs/specs/changelogs as part of the product contract, and ensure they exactly match current behavior, supported formats, and rendering constraints.

Apply this checklist before merge:
- **Exact formats and constraints**: Document the real file path/inputs/encodings verbatim; spell out quoting, casing, separators, and normalization rules that would otherwise fail silently. Remove or update examples that imply unsupported behavior.
- **Render correctness**: Use markdown that actually renders in your target UI (e.g., link PRs with `[#1234](https://...)`; prefer Unicode emojis over `:sparkles:` style shortcodes if the renderer can’t resolve them).
- **Keep latest-source parity**: When drafts exist across channels (e.g., Slack vs repo), explicitly sync to the latest intended content; don’t merge outdated emoji/text/version bullets.
- **Spec mirrors UX/implementation**: When product direction changes (modal → inline editor, renamed interaction patterns), update the spec to match the real interaction model and state transitions.
- **Avoid brittle claims**: Don’t encode “too-strong” invariants that the system doesn’t truly own; qualify requirements to what the product guarantees.

Example (configuration doc precision):
```yaml
# Flat YAML map: action_name -> key_trigger
# action_name contains ':' so it must be quoted
"workspace:toggle_ai_assistant": ctrl-s
"editor_view:delete_all_left": cmd-shift-A
"workspace:toggle_command_palette": none
```

Example (changelog rendering):
- Use `[#9275](https://github.com/warpdotdev/warp/pull/9275)`.
- Use Unicode emojis like `✨` instead of `:sparkles:` when shortcode rendering isn’t available.