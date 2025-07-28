---
title: Use contextually descriptive names
description: Names should clearly indicate their purpose and context to avoid confusion,
  especially when similar concepts exist in the same scope. Generic names like "api",
  "params", or "arg1" create ambiguity and make code harder to understand. Instead,
  use specific, meaningful identifiers that describe what they represent or do.
repository: mastodon/mastodon
label: Naming Conventions
language: TSX
comments_count: 5
repository_stars: 48691
---

Names should clearly indicate their purpose and context to avoid confusion, especially when similar concepts exist in the same scope. Generic names like "api", "params", or "arg1" create ambiguity and make code harder to understand. Instead, use specific, meaningful identifiers that describe what they represent or do.

Examples of improvements:
- Change generic labels like "expand"/"collapse" to contextual ones like "Expand/collapse lists menu"
- Replace confusing names like `params` (which resembles `useParams` hook) with descriptive alternatives like `target`
- Use meaningful parameter names like `index` instead of generic `arg1`, `arg2`
- Replace non-specific names like `api` with descriptive alternatives that indicate their actual purpose

This practice becomes especially important when multiple similar concepts exist in the same scope, as clear naming prevents confusion and improves code maintainability.