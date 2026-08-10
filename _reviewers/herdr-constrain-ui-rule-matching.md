---
title: Constrain UI Rule Matching
description: 'When building text-based state detectors (e.g., parsing a live UI/pane),
  treat each rule like an algorithmic classifier: make matches precise by localizing
  the search, anchoring invariants, and gating multi-step prompts.'
repository: ogulcancelik/herdr
label: Algorithms
language: Toml
comments_count: 3
repository_stars: 26924
---

When building text-based state detectors (e.g., parsing a live UI/pane), treat each rule like an algorithmic classifier: make matches precise by localizing the search, anchoring invariants, and gating multi-step prompts.

Apply these rules:
1) Localize to the expected live region
- Use the buffer/region where the live control actually appears (e.g., bottom chrome for footer buttons). Avoid `whole_recent` unless you’ve proven no stale history can match.

2) Anchor to UI invariants (full-line where possible)
- Prefer regexes that require exact placement/shape of the UI token. For prompts that are a single glyph, enforce full-line equality.

3) Add explicit gates for multi-part prompts
- If a state is identified by a sequence (header + specific question), gate the rule with a constrained region and an anchored/structured regex (and include negative tests for copied/offscreen text).

Example (TOML-style rules):
```toml
# Working: match a live footer invariant, only in bottom chrome
[[rules]]
id = "working_esc_interrupt"
state = "working"
priority = 900
region = "bottom_non_empty_lines(8)"
visible_working = true
contains = ["esc to interrupt"]

# Idle: require the prompt is a single glyph on its own line
[[rules]]
id = "idle_prompt"
state = "idle"
priority = 700
region = "bottom_non_empty_lines(5)"
visible_idle = true
line_regex = ['^\s*⟩\s*$']

# Blocked trust: gate with region + anchored header+question pattern
[[rules]]
id = "trust_directory"
state = "blocked"
priority = 950
region = "top_non_empty_lines(20)"
visible_blocker = true
regex = ['(?s)\A> You are in[^\r\n]+\r?\n\s*\r?\n\s*Do\s+you\s+trust']
```

Outcome: fewer false positives from scrolled history or copied dialog text, and more stable state transitions across UI variations.