---
title: Ensure deterministic resume behavior
description: When implementing persistence and resume functionality in durable execution
  systems, ensure that state is persisted at consistent event boundaries and that
  resume logic handles all execution states explicitly to maintain deterministic behavior.
repository: strands-agents/sdk-python
label: Temporal
language: Python
comments_count: 4
repository_stars: 4044
---

When implementing persistence and resume functionality in durable execution systems, ensure that state is persisted at consistent event boundaries and that resume logic handles all execution states explicitly to maintain deterministic behavior.

Key principles:
1. **Choose appropriate persistence timing**: Persist state at events that provide clear recovery semantics. For example, persisting on `BeforeNodeCallEvent` ensures that if execution crashes during a node, resume will restart from that node rather than an earlier point.

2. **Handle terminal states explicitly**: When resuming from terminal states (COMPLETED, FAILED), determine whether to restart execution or return previous results based on clear business logic.

3. **Avoid state corruption during resume**: Don't automatically clear failed nodes or modify execution state during resume unless there's explicit justification, as this can alter the original execution path.

Example of proper state handling:
```python
def deserialize_state(self, payload: dict) -> None:
    # Handle terminal states explicitly
    if payload.get("status") in (Status.COMPLETED.value, Status.FAILED.value):
        if not payload.get("next_nodes_to_execute"):
            # Execution ended - reset for new run
            self._reset_state()
            return
    
    # Resume from persisted state without modifying execution path
    self._restore_state(payload)
    # Don't clear failed_nodes - preserve original execution semantics
```

This ensures that durable execution systems behave predictably across interruptions and restarts, maintaining the integrity of the workflow orchestration.