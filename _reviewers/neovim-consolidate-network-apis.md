---
title: consolidate network APIs
description: When implementing network functionality, consolidate around standardized
  APIs like `vim.net.request()` instead of maintaining custom download functions or
  direct curl calls. Implement comprehensive testing for network operations using
  integration test guards to prevent failures in environments without network access.
repository: neovim/neovim
label: Networking
language: Other
comments_count: 4
repository_stars: 91433
---

When implementing network functionality, consolidate around standardized APIs like `vim.net.request()` instead of maintaining custom download functions or direct curl calls. Implement comprehensive testing for network operations using integration test guards to prevent failures in environments without network access.

Key practices:
- Replace custom download/HTTP functions with `vim.net.request()`
- Guard network-dependent tests with environment variables (e.g., `NVIM_TEST_INTEG`)
- Test both text and binary response handling
- Use `t.skip()` to conditionally skip network tests when integration testing is disabled

Example implementation:
```lua
-- Instead of custom download functions
local function download(url)
  -- Replace with vim.net.request()
end

-- Proper test guarding
describe('network functionality', function()
  local skip_integ = os.getenv('NVIM_TEST_INTEG') ~= '1'
  
  it('handles text responses', function()
    if skip_integ then t.skip() end
    -- network test implementation
  end)
  
  it('handles binary responses', function()
    if skip_integ then t.skip() end
    -- binary response test
  end)
end)
```

This approach ensures consistent network handling across the codebase while maintaining testability in various environments.