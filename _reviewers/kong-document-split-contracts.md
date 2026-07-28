---
title: Document Split Contracts
description: 'When implementing algorithmic transformations that clients depend on
  (especially split/partition functions and any logic that rebuilds/serializes structured
  strings), treat semantics as a stable API: explicitly define and document the contract
  (edge cases, limits, nil/empty handling, delimiter rules), and guarantee deterministic
  output by not relying on...'
repository: Kong/kong
label: Algorithms
language: Other
comments_count: 9
repository_stars: 43871
---

When implementing algorithmic transformations that clients depend on (especially split/partition functions and any logic that rebuilds/serializes structured strings), treat semantics as a stable API: explicitly define and document the contract (edge cases, limits, nil/empty handling, delimiter rules), and guarantee deterministic output by not relying on non-deterministic table iteration.

Practical rules:
- Splitters/partitioners: write the expected behavior for `value=nil`, `value==""`, `pattern==nil`, `pattern==""`, and how `n`/max is honored (never more than `n`, what the last element contains, etc.).
- Plain vs pattern: document whether the delimiter is treated as a literal string or a pattern, and how empty delimiters behave.
- Deterministic serialization: if you rebuild a query/string from a map, iterate keys in a deterministic order (e.g., sorted keys) and preserve repeated-parameter semantics (don’t silently collapse multiple values).
- Add targeted tests for the trickiest semantic boundaries (limit=0/1, empty delimiter, delimiter longer than input, boundary windows, etc.).

Example (deterministic query rebuild while avoiding `pairs` ordering issues):
```lua
local function rebuild_query_in_order(kv)
  local keys = {}
  for k in pairs(kv) do
    keys[#keys+1] = k
  end
  table.sort(keys)

  local parts = {}
  for i = 1, #keys do
    local k = keys[i]
    local v = kv[k]
    -- If kv[k] can have repeated values, encode accordingly; otherwise keep single.
    parts[#parts+1] = k .. "=" .. v
  end
  return table.concat(parts, "&")
end
```