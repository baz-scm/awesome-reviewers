---
title: reduce test verbosity
description: Write concise, efficient tests by eliminating repetitive code and combining
  related test cases. Avoid verbose patterns that can be simplified with better approaches.
repository: neovim/neovim
label: Testing
language: Other
comments_count: 8
repository_stars: 91433
---

Write concise, efficient tests by eliminating repetitive code and combining related test cases. Avoid verbose patterns that can be simplified with better approaches.

Key strategies:
- Use multiline patterns instead of multiple `screen:expect()` calls with `unchanged=true`
- Write literal contents when known rather than using generic matchers like `{MATCH: +}`
- Combine related test cases into single tests when they save significant code (20+ lines)
- Create shared functions for tests that follow similar patterns
- Reuse existing test setup and assertions instead of creating new ones
- Keep validation tests concise - checking that a command requires an argument should only need ~2 lines

Example of verbose vs. concise screen testing:
```lua
-- Verbose (avoid):
screen:expect({ any = '.nvim.lua' })
screen:expect({ any = pesc('[i]gnore, (v)iew, (d)eny:'), unchanged = true })

-- Concise (prefer):
screen:expect({ any = 'Allowed.*\n.exrc' })
```

The goal is maintainable tests that clearly express intent without unnecessary repetition or complexity.