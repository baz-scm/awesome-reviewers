---
title: Behavior-Accurate Doc Standards
description: 'Technical documentation (especially CLI/reference and machine-readable
  formats) must be implementation-faithful and user-actionable: don’t describe features/options
  that are ignored, don’t leave ambiguous exception behavior unexplained, and ensure
  examples and schemas match real parsing/output.'
repository: cline/cline#v4
label: Documentation
language: Other
comments_count: 4
repository_stars: 70864
---

Technical documentation (especially CLI/reference and machine-readable formats) must be implementation-faithful and user-actionable: don’t describe features/options that are ignored, don’t leave ambiguous exception behavior unexplained, and ensure examples and schemas match real parsing/output.

Apply these rules:
1) Match implementation precisely
- If behavior differs from what readers might assume, document the real behavior (e.g., remove misleading rows rather than saying “accepted but ignored”).
- Keep tables aligned with runtime semantics (e.g., ordering, defaults, inclusion/exclusion).

2) Add explicit “caveats” blocks for non-obvious exceptions
- When behavior depends on provider/provider-class, platform, or runtime mode, add a short, labeled caveat that explains what changes and why users may observe different outcomes.

3) For CLI/JSON interfaces: specify the exact wire format
- Document the exact structure (e.g., “one JSON object per line”), required discriminator fields, and what types are safe/expected to be parsed by scripts.

4) Examples must follow real argument parsing
- Ensure example command lines place options in the positions the parser expects.
- When an ordering constraint is non-obvious, include a brief “why” so users don’t repeat the mistake.

Example (schematized JSON output):
```text
With --json, the CLI prints one JSON object per line.
Every line has:
- type: discriminator
- ts: ISO 8601 timestamp
Only parse the line types intended for scripts.
```

Example (argument ordering rationale):
```bash
# Put connector options before the channel because the CLI forwards everything after the channel.
cline connect telegram --restart -k <BOT-TOKEN>
```