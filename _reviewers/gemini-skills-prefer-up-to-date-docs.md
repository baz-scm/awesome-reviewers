---
title: Prefer up-to-date docs
description: When building Gemini/LLM integrations, always use the most current and
  indexed API documentation/spec first, and avoid inefficient fallback behaviors.
repository: google-gemini/gemini-skills
label: AI
language: Markdown
comments_count: 2
repository_stars: 3451
---

When building Gemini/LLM integrations, always use the most current and indexed API documentation/spec first, and avoid inefficient fallback behaviors.

Apply this standard:
- If MCP tool `search_documentation` is available: treat it as the only documentation source.
  - Call `search_documentation`, read the returned docs, and then generate code immediately.
  - Do not manually fetch URLs.
  - Do not fall back to `llms.txt` after MCP already provided sufficient information.
  - Cap documentation lookups (e.g., maximum 2 tool calls) before generating output.
- If MCP is not available: use the official docs index (`llms.txt`) to discover pages, then fetch only the specific needed pages.
- For API schemas/fields/operations: use the REST API discovery spec as the source of truth (default v1beta; use v1 only when explicitly pinned).
- When adding new skills (e.g., Interactions API), prevent use of deprecated SDKs and base/test your implementation against the existing `gemini-api-dev` skill examples.

Example (MCP-first behavior):
```text
IF tool search_documentation exists:
  docs = search_documentation("How to call Structured Outputs in Gemini")
  // Ensure docs are sufficient
  generate code using docs
  // Do NOT fetch llms.txt as a fallback
ELSE:
  fetch llms.txt index
  fetch only the needed page(s)
  generate code using fetched docs
```