---
title: Semantic Identifier Consistency
description: 'Use names that (a) match the authoritative contract and (b) truthfully
  describe what the code does—consistently across upstream, models, and outputs.

  '
repository: awslabs/mcp
label: Naming Conventions
language: Python
comments_count: 7
repository_stars: 9545
---

Use names that (a) match the authoritative contract and (b) truthfully describe what the code does—consistently across upstream, models, and outputs.

Apply these rules:
- **Match source-of-truth naming end-to-end:** If upstream metadata/SDK/UI uses `parameters` (e.g., `SHOW DATABASES`), rename your model field to `parameters` and update all downstream usage (avoid aliases that reintroduce ambiguity).
- **Be consistent by layer:** If you standardize tool outputs (e.g., sibling tools) use the agreed wrapper keys/casing consistently (e.g., `data.procurement_portal_preferences` in snake_case), while preserving upstream field casing within the payload when that’s the contract (e.g., keep per-item PascalCase if the API returns it).
- **Name helpers by behavior:** Rename utilities so their names reflect what they actually generate/do (e.g., `_sql_identifier()` for identifier-building, not `_sql_string_literal()`), and ensure the implementation matches the meaning.
- **Avoid confusing or generic pattern names:** Prefer module/file names that accurately describe the component’s responsibility (e.g., choose `executor.py` over `pipeline.py` when it’s not a pipeline abstraction).
- **Make config inputs unambiguous:** Don’t expose multiple overlapping parameters (e.g., `endpoint` + `endpoint_url`) unless they’re clearly distinguished; prefer a single override-style parameter name or derive one from the other.
- **If naming is derived from external strings, validate safety:** When you derive column/table identifiers from API names, enforce safe identifier rules (and handle reserved keywords if applicable).

Quick example (wrapper vs payload casing):
```python
# Standardized wrapper key (snake_case) for consistency
return {
    "data": {
        "procurement_portal_preferences": raw_api_response[
            "ProcurementPortalPreferences"
        ]
    }
}
# Keep item fields as provided by the API contract (PascalCase)
# e.g., item dict keys remain what the API returns.
```