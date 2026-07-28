---
title: Observability semantic contract
description: 'Establish an explicit observability contract in code: tracing spans
  must be finished centrally with correct semantics; trace context inputs must be
  validated/formatted to standards; metrics must not mix different meanings across
  streaming vs non-streaming.'
repository: apache/apisix
label: Observability
language: Other
comments_count: 7
repository_stars: 16922
---

Establish an explicit observability contract in code: tracing spans must be finished centrally with correct semantics; trace context inputs must be validated/formatted to standards; metrics must not mix different meanings across streaming vs non-streaming.

Apply these rules:
1) Centralize span finishing on exit/error
- Finish spans in common response exit paths so you don’t rely on “every caller remembering.” Prefer error/exit thresholds (e.g., `code >= 400`) and/or provide a shared tracer utility to finish any pending spans.

2) Validate/format W3C traceparent inputs
- Never treat arbitrary IDs as `trace_id` unless they match W3C requirements (32 lowercase hex chars). If you must derive from a UUID/request id, transform it (e.g., remove hyphens) or fall back to generated IDs.

3) Use OTEL semantic convention attribute keys
- Prefer the canonical OTEL names (e.g., `http.response.status_code`) to keep dashboards and tools consistent.

4) Define metric meaning per request mode
- Don’t reuse one metric series for multiple “time” definitions. For AI streaming, record TTFT separately from total completion latency; for non-streaming, avoid writing TTFT-at-a-single-moment distributions.

Example patterns (illustrative):
```lua
-- 1) Finish spans on error in a shared exit path
if code and code >= 400 then
  tracer.finish_current_span(tracer.status.ERROR, message or ("response code " .. code))
end

-- 2) Validate W3C trace_id when building traceparent
local function is_valid_trace_id(id)
  return type(id) == "string" and id:match("^%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x$")
end

local trace_id = incoming_trace_id
if not is_valid_trace_id(trace_id) then
  trace_id = uuid.generate_v4() -- or transform/remove hyphens from UUID
end

-- 3) OTEL semantic convention
span:set_attributes(attr.int("http.response.status_code", upstream_status))

-- 4) Metrics split by request type
if vars.request_type == "ai_stream" then
  metrics.apisix_llm_ttft:observe(ttft_ms, labels)
  -- apisix_llm_latency should represent total completion latency for streaming
end
```

Result: consistent tracing shutdown, standards-compliant context propagation, tool-friendly semantic attributes, and metric series that remain interpretable for alerts and SLOs.