---
title: Unified extension API contracts
description: When building WebUI plugin/extension systems, treat the backend as the
  source of truth for (1) resolving extension contents and (2) providing a stable
  context schema to JS extensions.
repository: agent0ai/agent-zero
label: API
language: JavaScript
comments_count: 2
repository_stars: 17612
---

When building WebUI plugin/extension systems, treat the backend as the source of truth for (1) resolving extension contents and (2) providing a stable context schema to JS extensions.

Apply these rules:

- Extension-point resolution: When the client finds an element like `<x-extension id="...">`, it should call a dedicated backend API (e.g., `get_webui_extensions(id)`) that searches the plugin roots by convention (e.g., `.../extensions/webui/{id}/*.html`) and returns the HTML/content to paste into that node. Keep the client loader thin; avoid re-implementing manifest/scan logic when the backend can resolve by id.

- Stable context schema: Ensure `callJsExtensions(..., context)` uses one unified “context” shape across default and custom message handlers. If an extension needs `message.no` (log number), that field must be present consistently in the default implementation too.

Example (contract-driven usage):
```js
// Client: paste extension HTML resolved by backend
async function applyExtensionPoint(node, id) {
  const htmlParts = await get_webui_extensions(id); // backend contract
  node.innerHTML = htmlParts.join("\n");
}

// JS extension: rely on unified context schema
export default async function injectBranchButtons(context) {
  const msgs = context?.messages;
  if (!Array.isArray(msgs) || msgs.length === 0) return;

  for (const m of msgs) {
    // contract requires log number (no)
    if (typeof m.no !== "number") throw new Error("Missing context.messages[].no");
    // ...use m.no to wire actions
  }
}
```

Outcome: frontend extension code becomes deterministic (no “sometimes field is present” surprises), and plugin authors can build against a predictable backend-defined contract.