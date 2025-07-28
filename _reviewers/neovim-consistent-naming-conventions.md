---
title: consistent naming conventions
description: Maintain consistent naming patterns and terminology across the codebase
  to reduce cognitive load and improve code clarity. The same concept should always
  use the same name in different contexts.
repository: neovim/neovim
label: Naming Conventions
language: Other
comments_count: 8
repository_stars: 91433
---

Maintain consistent naming patterns and terminology across the codebase to reduce cognitive load and improve code clarity. The same concept should always use the same name in different contexts.

Key principles:
- Use established prefixes: `on_` for event handlers/callbacks, `is_` for boolean predicates, `get_` for accessors
- Follow codebase conventions: use `start`/`end` for ranges, `refresh()` for common update operations
- Avoid confusing similar terms: distinguish between "mode" and "modal", use descriptive names over generic ones
- Use consistent terminology across interfaces: if you call something "position" in one place, don't call it "location" elsewhere

Examples:
```lua
-- Good: consistent callback naming
function on_document_highlight(err, result, ctx) end

-- Bad: inconsistent suffix
function document_highlight_cb(err, result, ctx) end

-- Good: consistent terminology
local function get_logical_pos(diagnostic) end

-- Bad: mixing terminology  
local function get_logical_location(diagnostic) end

-- Good: established convention
local mark = { start_line = start_row, start_col = start_col }

-- Bad: non-standard naming
local mark = { begin_line = start_row, begin_col = start_col }
```

When introducing new names, check existing code for established patterns. Consistency trumps personal preference - if the codebase uses a particular naming convention, follow it even if you prefer alternatives.