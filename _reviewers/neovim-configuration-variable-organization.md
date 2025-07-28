---
title: Configuration variable organization
description: Use structured naming patterns and avoid polluting the global namespace
  when managing configuration variables. Prefer storing configuration state on relevant
  objects rather than creating numerous top-level global variables.
repository: neovim/neovim
label: Configurations
language: Other
comments_count: 4
repository_stars: 91433
---

Use structured naming patterns and avoid polluting the global namespace when managing configuration variables. Prefer storing configuration state on relevant objects rather than creating numerous top-level global variables.

For naming patterns, use separators like ":" to distinguish variable components:
```lua
-- Good: structured naming with clear separation
local function get_client_augroup(client_id)
  return 'nvim.lsp.linked_editing_range.client:' .. client_id
end
```

When dealing with client-specific or feature-specific configuration, consider storing the data directly on the relevant object instead of creating many global variables:
```lua
-- Instead of: many global variables like __lsp_feature_client_42_enabled
-- Prefer: storing on the client object itself
client._feature_enabled = true
```

For complex configuration hierarchies, use nested tables rather than flat naming schemes:
```lua
-- Good: organized structure
_lsp_enable = {
  client = { [42] = true, [78] = true },
  feature = { hover = true, completion = false }
}

-- Avoid: namespace pollution
-- __lsp_hover_client_42_enabled = true
-- __lsp_completion_client_78_enabled = false
```

This approach reduces global namespace pollution, improves code maintainability, and makes configuration relationships more explicit.