---
title: Sanitize Model Output
description: When handling untrusted model/text output that will be serialized into
  JSON (or rendered in a UI), normalize it before output generation—specifically strip
  or escape tag-like content (e.g., “<think>…</think>”) so it cannot corrupt JSON
  or break downstream parsing.
repository: agent0ai/agent-zero
label: Security
language: Other
comments_count: 1
repository_stars: 17612
---

When handling untrusted model/text output that will be serialized into JSON (or rendered in a UI), normalize it before output generation—specifically strip or escape tag-like content (e.g., “<think>…</think>”) so it cannot corrupt JSON or break downstream parsing.

Apply this by adding a single sanitization/normalization step right before JSON serialization (or right before writing responses to clients):

```js
function sanitizeTagsByLine(text) {
  return text
    .split(/\r?\n/)
    .map(line => line
      // remove thinking tags that can break JSON/UI parsing
      .replace(/<\s*think\s*>[\s\S]*?<\s*\/\s*think\s*>/gi, "")
      // optionally remove any stray <think> tags
      .replace(/<\s*think\s*>/gi, "")
      .replace(/<\s*\/\s*think\s*>/gi, "")
    )
    .join("\n");
}

const raw = modelOutputText; // untrusted
const safe = sanitizeTagsByLine(raw);
const json = JSON.stringify({ content: safe });
```

Also add a quick sanity check (e.g., ensure the produced payload is valid JSON and the UI receives expected fields) so tag-related issues are caught early.