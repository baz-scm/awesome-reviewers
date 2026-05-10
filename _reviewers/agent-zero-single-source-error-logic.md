---
title: Single Source Error Logic
description: 'When handling failures or optional data, make the decision exactly once
  and reuse the result everywhere.


  Apply two concrete rules:

  1) **Normalize once, then use the normalized values for both validation and execution.**
  Don’t validate one set of fields and execute using separately-fallbacked canonical
  fields.'
repository: agent0ai/agent-zero
label: Error Handling
language: Python
comments_count: 2
repository_stars: 17612
---

When handling failures or optional data, make the decision exactly once and reuse the result everywhere.

Apply two concrete rules:
1) **Normalize once, then use the normalized values for both validation and execution.** Don’t validate one set of fields and execute using separately-fallbacked canonical fields.
2) **Centralize optional-feature degradation.** Don’t repeat broad `try/except` import patterns across many call sites—move them into a shared helper that returns either the real implementation or a safe no-op.

Example (canonicalize before validate/execute):
```python
def normalize_tool_request(payload: dict) -> tuple[str, dict] | None:
    # pick a single canonical source-of-truth (fallbacking happens only here)
    tool_name = payload.get("tool_name") or payload.get("tool")
    tool_args = payload.get("tool_args") or payload.get("args")
    if not tool_name or tool_args is None:
        return None
    return tool_name, tool_args

async def process_tools(self, msg: str):
    tool_request = extract_tool_request(msg)  # returns dict or None
    if tool_request is None:
        return

    normalized = normalize_tool_request(tool_request)
    if normalized is None:
        return  # structural/misformat handled once

    tool_name, tool_args = normalized
    await self.validate_tool_request({"tool_name": tool_name, "tool_args": tool_args})
    # execution uses tool_name/tool_args derived from the same normalized result
    await self.execute_tool(tool_name, tool_args)
```

Example (centralize optional integration):
```python
# python/helpers/state_monitor.py
def get_state_monitor():
    try:
        from python.helpers.state_monitor_impl import StateMonitor
        return StateMonitor()
    except ImportError:
        return None  # safe degraded mode

# call site
monitor = get_state_monitor()
if monitor is not None:
    monitor.state_push(...)
```

This prevents inconsistent “validation passes but execution breaks” flows and reduces duplicated, inconsistent error-handling paths for optional integrations.