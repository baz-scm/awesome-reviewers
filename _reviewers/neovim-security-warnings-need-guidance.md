---
title: Security warnings need guidance
description: Security-related warnings and error messages should provide clear, actionable
  guidance on how users can safely resolve the issue, not just inform them of the
  problem. When displaying security warnings, include specific instructions that guide
  users through the secure workflow.
repository: neovim/neovim
label: Security
language: Other
comments_count: 1
repository_stars: 91433
---

Security-related warnings and error messages should provide clear, actionable guidance on how users can safely resolve the issue, not just inform them of the problem. When displaying security warnings, include specific instructions that guide users through the secure workflow.

For example, instead of just stating a file is untrusted:
```lua
local msg = cwd .. pathsep .. 'Xfile is not trusted.'
```

Provide clear next steps:
```lua
local msg = cwd .. pathsep .. 'Xfile is not trusted. To enable it, choose (v)iew then run `:trust`.'
```

This approach helps users understand both the security concern and the proper way to address it, reducing the likelihood of unsafe workarounds or user confusion.