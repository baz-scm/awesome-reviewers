---
title: Document actual behavior
description: Documentation must reflect what the product actually does right now,
  not what it used to do, what it's supposed to do, or what a flag claims to do but
  doesn't. Before publishing or updating docs, verify defaults, option behavior, and
  claims against the current source code or implementation (e.g., confirm a CLI flag's
  documented default matches the code's...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Documentation
language: Other
comments_count: 6
repository_stars: 70986
---

Documentation must reflect what the product actually does right now, not what it used to do, what it's supposed to do, or what a flag claims to do but doesn't. Before publishing or updating docs, verify defaults, option behavior, and claims against the current source code or implementation (e.g., confirm a CLI flag's documented default matches the code's actual fallback value). If a feature, flag, or environment variable has been deprecated, removed, or silently stopped working, don't document it as if it still functions — either delete the stale entry or, if it must be mentioned (e.g., for migration/deprecation notices), state clearly what happens now and point to a working alternative. Avoid documenting "accepted but ignored" options, since that invites readers to rely on something that has no effect; instead omit the option or remove it from the interface. When describing coverage (e.g., "this reference lists every event type" or "this control is enforced"), use precise wording that matches reality — prefer narrower, accurate claims ("skip event types you don't recognize," "supports" instead of "enforces" when the behavior can be overridden by the user) over broad claims that don't hold up. When in doubt, favor removing or simplifying documentation for broken or non-core functionality over leaving misleading text in place, and track any follow-up fixes separately so docs stay trustworthy in the meantime.