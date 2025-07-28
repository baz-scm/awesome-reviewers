---
title: Complete function documentation
description: Ensure all functions have comprehensive, accurate documentation including
  required tags (@param, @return, @since), clear descriptions that match actual behavior,
  and explanatory comments for complex logic.
repository: neovim/neovim
label: Documentation
language: Other
comments_count: 7
repository_stars: 91433
---

Ensure all functions have comprehensive, accurate documentation including required tags (@param, @return, @since), clear descriptions that match actual behavior, and explanatory comments for complex logic.

Functions should include:
- All parameter descriptions with correct types
- Return value documentation that accurately describes what's returned
- Version tags (@since) for new features
- Brief explanatory comments for non-obvious code blocks

Example of complete documentation:
```lua
--- Makes an HTTP GET request to the given URL.
--- Can either return the body or save it to a file.
---
--- @param url string The URL to fetch.
--- @param opts? table Optional parameters:
---   - verbose (boolean|nil): Enables curl verbose output.
---   - retry   (integer|nil): Number of retries on transient failures (default: 3).
---   - output  (string|nil): If set, path to save response body instead of returning it.
--- @param on_exit? fun(err?: string, content?: string) Optional callback for async execution
--- @return string|boolean|nil Response body on success; `nil` on failure
--- @since 14
function M.get(url, opts, on_exit)
  -- Compute positions, set them as extmarks, and store in diagnostic._extmark_id
  -- (used by get_logical_location to adjust positions)
  once_buf_loaded(bufnr, function()
    -- complex logic here
  end)
end
```

Avoid confusing wording, inaccurate descriptions, or missing required documentation tags. Future developers should be able to understand the function's purpose, parameters, and behavior without studying the implementation.