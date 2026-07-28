---
title: Isolate config state
description: Configurable behavior must be isolated per plugin/consumer instance,
  and derived/internal values must not be injected into the schema-defined `conf`
  object. This prevents cross-request/config leakage and keeps schema validation predictable—especially
  during deprecations.
repository: Kong/kong
label: Configurations
language: Other
comments_count: 3
repository_stars: 43871
---

Configurable behavior must be isolated per plugin/consumer instance, and derived/internal values must not be injected into the schema-defined `conf` object. This prevents cross-request/config leakage and keeps schema validation predictable—especially during deprecations.

Apply:
- Don’t store per-config options in module-level locals (shared by all instances/requests in the same worker). Store them on an instance/table created per consumer/plugin.
- Treat `conf` as schema input: if you need computed/compiled data, create a separate table and pass it alongside `conf`.
- When introducing deprecated/new config fields, ensure both sides resolve/validate consistently for reference/vault values; don’t rely on `replaced_with` to “magically” reconcile dereferencing.

Example (instance-scoped state instead of module locals):
```lua
-- BAD: module-level mutable config shared across instances
-- local use_proto_names = false
-- function protojson:configure(options) use_proto_names = options.use_proto_names end

-- GOOD: store config on the instance
local protojson = {}
protojson.__index = protojson

function protojson.new(options)
  return setmetatable({
    use_proto_names = options.use_proto_names or false,
    enum_as_name = options.enum_as_name or false,
    emit_defaults = options.emit_defaults or false,
    json_names = options.json_names or {},
  }, protojson)
end

function protojson:decode_to_json(msg_type, msg)
  -- use self.use_proto_names etc.
end
```
Example (don’t mutate `conf` with non-schema fields):
```lua
function OpenTelemetryHandler:log(conf)
  local options = {}
  if conf.resource_attributes then
    options.compiled_resource_attributes = otel_utils.read_resource_attributes(conf.resource_attributes)
  end
  otel_traces.log(conf, options) -- pass alongside conf
end
```
