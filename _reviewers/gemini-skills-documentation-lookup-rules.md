---
title: Documentation lookup rules
description: 'When writing or updating API skill docs, treat documentation as an operational
  dependency: prefer the most up-to-date source, keep docs self-contained, and make
  examples unambiguous.'
repository: google-gemini/gemini-skills
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 3451
---

When writing or updating API skill docs, treat documentation as an operational dependency: prefer the most up-to-date source, keep docs self-contained, and make examples unambiguous.

Apply these rules:
1) **Prefer live indexed documentation (MCP) when available**
   - If an indexed doc tool like `search_documentation` exists, use it as the only doc source.
   - Don’t fetch URLs manually when MCP tools are present.
   - After getting the needed syntax/fields, **generate the code immediately** (avoid long re-check cycles).
2) **Make docs portable and discoverable**
   - Avoid relative links that break in isolated contexts (e.g., `../...`). Use stable full paths or inline the required guidance.
   - Ensure new skills are listed/linked from the project’s main docs, and structure docs to avoid duplication.
3) **Define key terms explicitly**
   - If the API distinguishes concepts (e.g., **model** vs **agent**), define what each means and when to set each.
4) **Specify example placeholder types and formats**
   - For any placeholder like `frame`, document the expected type/encoding (e.g., bytes, base64 string, MIME type, tensor) so developers can pass correct inputs.

Example (self-contained documentation snippet):
```python
# `frame` must be raw bytes for a single image frame, encoded as JPEG/PNG bytes
# (or provide the required mime_type for the SDK wrapper).
# If you pass base64 strings, convert them to bytes (or use the SDK's expected field type).

await session.send_realtime_input(
    video=types.Blob(data=frame_bytes, mime_type="image/jpeg")
)
```

Use this checklist during review to prevent stale guidance, broken links, and “works in theory” examples that fail at integration time.