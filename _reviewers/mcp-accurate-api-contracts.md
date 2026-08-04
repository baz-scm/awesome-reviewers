---
title: Accurate API Contracts
description: 'For API/tool-facing code, treat the external API contract as non-negotiable:
  validate parameter bounds against the upstream model/docs, handle pagination only
  when the API is actually paginated, and ensure your client/tool surface (operation
  routing, errors, and side-effect metadata) is explicit and consistent.'
repository: awslabs/mcp
label: API
language: Python
comments_count: 9
repository_stars: 9545
---

For API/tool-facing code, treat the external API contract as non-negotiable: validate parameter bounds against the upstream model/docs, handle pagination only when the API is actually paginated, and ensure your client/tool surface (operation routing, errors, and side-effect metadata) is explicit and consistent.

Apply this checklist:
1) **Parameter constraints must match upstream**
   - Don’t mirror limits from similar APIs unless the upstream model/doc confirms it.
2) **Pagination must match upstream behavior**
   - If the API returns `NextToken`, loop until exhaustion (or a hard cap) so you don’t produce false negatives.
   - If the API is not paginated, don’t add pagination plumbing (it adds confusion and can hide logic errors).
3) **Operation routing should match shared parameter sets**
   - Use `operation`-routing when most ops share a core parameter set.
   - Split into separate tools/groups when parameter schemas diverge to avoid huge “optional soup” that reduces correctness.
   - For closely named operations/tools, include a **disambiguation block** in the description.
4) **Return a consistent error shape**
   - Keep `error` + `error_type` (or equivalent) uniform so clients/LLMs can reliably decide retry vs fix.
5) **Keep mutation-risk metadata truthful**
   - If a tool “may” be destructive, keep `destructiveHint=true` (don’t mark it additive-only).

Example: correct pagination loop + contract-aligned `max_results` validation
```python
from typing import Any, Dict, List, Optional


def validate_max_results(max_results: Optional[int]) -> Optional[int]:
    # Example of contract-aligned validation: 1–500 per AWS model
    if max_results is None:
        return None
    if not (1 <= max_results <= 500):
        raise ValueError("max_results must be between 1 and 500")
    return max_results


def call_paged_list_api(client, *, start: int, end: int, max_results: int = 100) -> List[Dict[str, Any]]:
    # Only do this if the upstream API is actually paginated and returns NextToken.
    results: List[Dict[str, Any]] = []
    next_token: Optional[str] = None

    while True:
        params = {
            "StartTime": start,
            "EndTime": end,
            "MaxResults": max_results,
        }
        if next_token:
            params["NextToken"] = next_token

        resp = client.list_something(**params)
        results.extend(resp.get("Items", []))

        next_token = resp.get("NextToken")
        if not next_token:
            break

        # Optional safety cap to prevent fan-out
        # if len(results) > 10_000: break

    return results
```

If you adopt this standard, you prevent the most common production failures seen in the discussions: silent truncation (missing pages), incorrect parameter ranges, ambiguous routing choices, and inconsistent error/side-effect semantics.