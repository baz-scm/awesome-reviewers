---
title: Semantic naming over implementation
description: Choose names that reflect the semantic purpose and meaning rather than
  implementation details or internal mechanisms. Names should communicate what something
  does or represents from the user's perspective, not how it works internally.
repository: neovim/neovim
label: Naming Conventions
language: Txt
comments_count: 4
repository_stars: 91433
---

Choose names that reflect the semantic purpose and meaning rather than implementation details or internal mechanisms. Names should communicate what something does or represents from the user's perspective, not how it works internally.

For example, prefer `on_response` over `on_exit` for HTTP request callbacks, since "response" describes the semantic event while "exit" exposes the internal detail that curl process exits. Similarly, use `version` to describe the semantic concept rather than `checkout` which exposes the Git implementation detail.

Follow established project conventions consistently:
- Use `on_` prefix for event-handling callbacks and handlers
- Use `callback` for continuation functions (single callback parameter)
- Apply naming patterns systematically across similar contexts

Example of good semantic naming:
```lua
-- Good: describes the semantic purpose
vim.net.request(url, opts, on_response)

-- Poor: exposes implementation detail  
vim.net.request(url, opts, on_exit)
```

When multiple naming options exist, prioritize the one that best communicates the intended use and meaning to other developers, while maintaining consistency with existing codebase patterns.