---
title: Document Stable API Contracts
description: All API reference docs (and examples) must clearly define the *public*
  contract vs *temporary/hidden* behavior, and keep endpoint paths/query params and
  response fields consistent.
repository: infiniflow/ragflow
label: API
language: Markdown
comments_count: 5
repository_stars: 80174
---

All API reference docs (and examples) must clearly define the *public* contract vs *temporary/hidden* behavior, and keep endpoint paths/query params and response fields consistent.

Apply:
- Add explicit caution notes for behavioral differences (e.g., streaming vs non-stream payload fields). If a field is unavailable, document it and how to obtain it (e.g., non-stream with raw response).
- Mark hidden/unstable parameters as such and state that they must not be treated as a stable public API.
- Ensure endpoint paths are formatted correctly (no accidental extra slashes) and query parameters in URLs match the documented schema.
- Provide practical request examples that cover common patterns, including multi-value/array query parameters.
- Keep response schema fields consistent across endpoints (e.g., don’t use `code` and `error_code` interchangeably without a documented rule).

Example pattern (streaming caveat):
```md
:::caution NOTE
`client.chat.completions.create(stream=True, ...)` does not return `reference`.
`reference` is only exposed in the non-stream response payload (or via raw non-stream mode).
Use non-stream to access `reference`.
:::
```