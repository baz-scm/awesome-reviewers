---
title: SSR documentation clarity
description: Ensure server-side rendering documentation is grammatically correct and
  clearly explains the differences between server and client contexts. Documentation
  should explicitly describe hydration behavior, performance implications, and function
  availability constraints.
repository: sveltejs/svelte
label: Next
language: Markdown
comments_count: 2
repository_stars: 83580
---

Ensure server-side rendering documentation is grammatically correct and clearly explains the differences between server and client contexts. Documentation should explicitly describe hydration behavior, performance implications, and function availability constraints.

When documenting SSR features, avoid ambiguous language and provide specific context about when certain behaviors occur. For example, instead of vague references to "render," specify whether you mean "server render" or "client render."

Example improvements:
- Change "If the a `{@html ...}` value changes" to "If the `{@html ...}` value changes"
- Clarify "not during the server render" vs "not during render" based on the specific context
- Explain performance rationale: "change detection during hydration is expensive and usually unnecessary"

This ensures developers understand SSR limitations and behaviors, reducing confusion during implementation and debugging.