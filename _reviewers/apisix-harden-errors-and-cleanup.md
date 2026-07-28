---
title: Harden Errors And Cleanup
description: 'Treat any external input (HTTP headers, JSON bodies, provider responses,
  dynamic config) as untrusted: validate its type/shape before indexing or string
  operations, and ensure errors don’t turn into uncontrolled 500s or leak state/resources.'
repository: apache/apisix
label: Error Handling
language: Other
comments_count: 7
repository_stars: 16922
---

Treat any external input (HTTP headers, JSON bodies, provider responses, dynamic config) as untrusted: validate its type/shape before indexing or string operations, and ensure errors don’t turn into uncontrolled 500s or leak state/resources.

Apply these rules:
- Validate before use: check types/structure (e.g., header could be a table; JSON may have unexpected scalar/shape). Return (nil, "…")/bypass with a clear log instead of letting `attempt to index a number/table` or `bad argument` escape.
- Make failures bounded: when reporting errors from third-party bodies, sanitize/bound the content; prefer status + a short reason over embedding full bodies.
- Keep retries correct: reset per-attempt flags/state at the entry of the operation being retried; never reuse a previous attempt’s “aborted/failed” marker.
- Cleanup must be unconditional: teardown and resource release must run even when handlers fail (use pcall for handler calls, then release in a finally-like path).
- Never poison connection pools: only `set_keepalive`/reuse a Redis (or cosocket) connection after the command succeeded; otherwise close.
- Prefer graceful handling over assert on remote data: log and skip/ignore invalid items instead of panicking.

Example pattern (Lua):
```lua
local function parse_embedding_response(core, raw_body)
  local data = core.json.decode(raw_body)
  if type(data) ~= "table" or type(data.data) ~= "table" then
    return nil, "invalid embedding response"
  end
  local vectors = {}
  for i, item in ipairs(data.data) do
    if type(item) ~= "table" then
      return nil, "invalid embedding entry at index " .. (i - 1)
    end
    -- safe field access after type checks
  end
  return vectors
end

local function with_redis(conf, fn)
  local red, err = redis_util.new(conf)
  if not red then return nil, err end
  local ok, res, rerr = pcall(fn, red)
  if not ok then
    red:close()
    return nil, res
  end
  -- only reuse after success
  local ok_keep, kerr = red:set_keepalive(conf.redis_keepalive_timeout, conf.redis_keepalive_pool)
  if not ok_keep then red:close() end
  return res
end
```