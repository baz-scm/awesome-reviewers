---
title: API surface compatibility
description: Treat any change to a public interface (PDK function signatures, plugin
  config/schema fields, or other externally-consumed API contracts) as a compatibility
  commitment.
repository: Kong/kong
label: API
language: Other
comments_count: 4
repository_stars: 43871
---

Treat any change to a public interface (PDK function signatures, plugin config/schema fields, or other externally-consumed API contracts) as a compatibility commitment.

**Do**
- **Avoid expanding public API surface** unless the benefit is clear and the tradeoffs are acceptable.
- If a function signature must change, **append new parameters at the end** (never insert in the middle) to preserve positional-arg compatibility.
- For **schema/config additions**: require a compatibility plan—discussion/approval, **changelog entry**, and any related compatibility/removed-fields plumbing (and tests that validate the schema).

**Don’t**
- Don’t add new public parameters that “paint you into a corner” without a strong necessity.
- Don’t change schema semantics/config options without coordinating compatibility artifacts.

**Example (signature change rule)**
```lua
-- Before
function compose_tags(service_name, status, consumer_id, tags, conf) end

-- After (append new param at the end)
function compose_tags(service_name, status, consumer_id, tags, conf, route_name) end
```

Apply this checklist whenever a change touches externally-defined contracts: if users (or other plugins) might call it, update it with backward compatibility as the default and a documented migration/compat story.