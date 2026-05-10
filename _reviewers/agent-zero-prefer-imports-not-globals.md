---
title: Prefer Imports, Not Globals
description: When wiring state/functions, avoid implicit access through `window.*`/`globalThis`.
  Use explicit ES module imports so code is deterministic and loads correctly, and
  keep code in the module/plugin that owns it.
repository: agent0ai/agent-zero
label: Code Style
language: JavaScript
comments_count: 4
repository_stars: 17612
---

When wiring state/functions, avoid implicit access through `window.*`/`globalThis`. Use explicit ES module imports so code is deterministic and loads correctly, and keep code in the module/plugin that owns it.

**Apply this standard**
- **Do import from the module** instead of fetching stores from `window` (including Alpine root store patterns).
- **Remove/avoid `window.Alpine?.store(...)` and `globalThis` bridging** for core dependencies; replace with imports.
- **Keep responsibilities local**: if a function is plugin-specific, implement it inside that plugin (not in a generic shared file).
- (Related) Extract small reusable UI helpers into local utilities when it reduces duplication.

**Example (store access)**
```js
// Prefer this:
import { createStore } from "/js/AlpineStore.js";
import { store as notificationStore } from "/components/notifications/notification-store.js";

// Avoid this pattern:
// const rootStore = window.Alpine?.store ? window.Alpine.store("root") : undefined;
// ...then rely on root/global wiring
```

**Checklist**
- No `window.Alpine.store('root')` just to get runtime state that has a dedicated module.
- No `globalThis` TODOs persisting long-term for dependencies—replace with imports.
- Plugin-only helpers live in the plugin module, not in shared infrastructure modules.