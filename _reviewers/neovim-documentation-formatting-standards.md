---
title: Documentation formatting standards
description: Ensure documentation follows consistent formatting standards to improve
  readability and maintainability. This includes proper indentation of code blocks
  for syntax highlighting, clear separation of examples with individual explanatory
  comments, and concise organization of related information.
repository: neovim/neovim
label: Code Style
language: Txt
comments_count: 3
repository_stars: 91433
---

Ensure documentation follows consistent formatting standards to improve readability and maintainability. This includes proper indentation of code blocks for syntax highlighting, clear separation of examples with individual explanatory comments, and concise organization of related information.

Key formatting requirements:
- Indent all code blocks properly for syntax highlighting to work correctly
- Provide separate, clear comments for each code example rather than grouping them under a single ambiguous comment
- Condense related bullet points or information into concise, single entries when possible

Example of improved formatting:
```lua
-- Install "plugin1" and use greatest available version
'https://github.com/user/plugin1',

-- Same as above, but using full table syntax for additional options
{ source = 'https://github.com/user/plugin2' },
```

Rather than:
```lua
-- Install as "plugin1"/"plugin2" and use greatest available version
'https://github.com/user/plugin1',
{ source = 'https://github.com/user/plugin2' },
```

This approach prevents confusion about whether examples represent single or multiple operations and ensures each example's purpose is immediately clear to readers.