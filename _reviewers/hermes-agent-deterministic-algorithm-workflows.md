---
title: Deterministic algorithm workflows
description: When you describe an algorithm (retrieval pipeline, scoring, ranking,
  etc.), ensure the implementation includes the complete promised workflow and produces
  deterministic outputs.
repository: nousresearch/hermes-agent
label: Algorithms
language: Markdown
comments_count: 2
repository_stars: 221948
---

When you describe an algorithm (retrieval pipeline, scoring, ranking, etc.), ensure the implementation includes the complete promised workflow and produces deterministic outputs.

Apply this checklist:
- **Scope matches claims**: If the doc claims “two-stage retrieval,” verify the code actually performs both retrieval passes, merges results, and invokes the intended path (or re-scope the claim to what’s implemented).
- **Make scoring/relevance computable**: Don’t rely on weights alone—define **per-check point values** and the exact formula that maps collected signals → final score.
- **Deterministic read-only collection**: Collect inputs in a **read-only** and repeatable way so repeated runs on the same state yield the same result (avoid time-dependent randomness, non-stable ordering, or modifying the host during collection).
- **Test reproducibility**: Add a small harness (or fixture) that runs the workflow twice on the same captured inputs and asserts identical outputs.

Example pattern (scoring determinism):
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Checks:
    ssh_root_login: bool
    open_ports: tuple[int, ...]   # ensure stable ordering
    updates_installed: bool

def score(checks: Checks) -> int:
    # Deterministic, explicit per-check points
    points = 0
    points += 25 if not checks.ssh_root_login else 0
    points += 25 if len(checks.open_ports) == 0 else max(0, 25 - 5*len(checks.open_ports))
    points += 20 if checks.updates_installed else 0
    # ... add the remaining dimensions with explicit point math
    return max(0, min(100, points))

def collect_read_only() -> Checks:
    # Only read system state; normalize ordering; no mutations
    open_ports = tuple(sorted(_read_open_ports()))
    return Checks(
        ssh_root_login=_read_ssh_root_login(),
        open_ports=open_ports,
        updates_installed=_read_updates_installed(),
    )
```

For retrieval workflows, use the same idea: document and implement every required step (index build, pass 1 retrieval, pass 2 expansion/retrieval, result merge, and the call site), or explicitly limit the documentation to the implemented subset.