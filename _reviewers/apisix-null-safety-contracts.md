---
title: Null Safety Contracts
description: When handling optional/nil values, treat nil as a real input only if
  it’s reachable; otherwise remove dead checks. More importantly, enforce clear contracts
  for types/shapes so nil never reaches code paths that assume a table/string.
repository: apache/apisix
label: Null Handling
language: Other
comments_count: 7
repository_stars: 16922
---

When handling optional/nil values, treat nil as a real input only if it’s reachable; otherwise remove dead checks. More importantly, enforce clear contracts for types/shapes so nil never reaches code paths that assume a table/string.

Practical rules:
1) Guard before indexing/iteration
- If a value may be nil, check it (and/or its type) before doing `x[y]`, `x:method()`, `pairs(x)`, or `table.concat`.

2) Preserve function return contracts
- Helpers that callers iterate over should return a safe type on all paths (e.g., always return `{}` instead of `nil` if the caller does `pairs(...)`).

3) Match conditional construction with downstream access
- If one branch omits a nested table (e.g., `body.index`), ensure later code doesn’t unconditionally access it. Either build the required structure in all branches or branch the downstream logic too.

4) Prefer explicit fallback over misleading nil branches
- If a nil-check is unreachable, delete it and use a forgiving fallback (e.g., `fetch_secrets(...) or upstream_obj`) to keep behavior correct in failure cases.

5) Tests: avoid vacuous “truthy encryption”
- When asserting that a value is encrypted, first require it’s a non-empty string; otherwise `nil ~= "plaintext"` will incorrectly pass.

Example patterns:
```lua
-- 1) fallback instead of dead nil-check
local new_upstream_ssl = apisix_secret.fetch_secrets(upstream_ssl, true)
new_upstream_ssl = new_upstream_ssl or upstream_ssl

-- 2) return safe type for iteration
local function names_from_proto(proto_obj)
  local names = {}
  if type(proto_obj) ~= "table" then
    return names
  end
  -- ... fill names
  return names
end

-- 3) nil-guard before method call
local data = core.request.get_body()
local ticket = data and data:match("<samlp:SessionIndex>(.+)</samlp:SessionIndex>")

-- 5) test: require non-empty string
local conf = get_conf()
local v = conf.client_rsa_private_key
assert(type(v) == "string" and v ~= "" and v ~= "plaintext")
```