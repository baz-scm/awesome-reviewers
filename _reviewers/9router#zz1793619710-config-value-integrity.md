---
title: Config value integrity
description: 'Every configuration value that code reads must be fully wired end-to-end:
  it needs a validated write path (API/DB), sane bounds checking, and must not be
  "fake" — i.e. don''t read `providerOverrides.timeoutMs` or similar fields if the
  route that persists overrides (e.g. `normalizeOverride`) silently strips them, leaving
  only an env var as the real knob....'
repository: decolua/9router#zz1793619710
label: Configurations
language: JavaScript
comments_count: 3
repository_stars: 31855
---

Every configuration value that code reads must be fully wired end-to-end: it needs a validated write path (API/DB), sane bounds checking, and must not be "fake" — i.e. don't read `providerOverrides.timeoutMs` or similar fields if the route that persists overrides (e.g. `normalizeOverride`) silently strips them, leaving only an env var as the real knob. Either implement full validation/persistence for the field or remove the dead read so the UI/config surface doesn't advertise a setting that can't actually be saved.

Default and disabled states must be honored exactly as documented. If a feature is "off until configured" (e.g. an empty `webSearchFallbackProvider`), don't silently infer or auto-pick a value when it's unset — that breaks the configuration contract and can route behavior through a provider/service the user never explicitly chose. Unset/empty should mean disabled, with a clear error/response surfaced to the caller, not a hidden fallback.

Finally, never hardcode values, model names, routing patterns, or role/block strings that are really configuration — move them into `config/` or `schema/` constants so they can be centrally validated, reused, and updated without touching business logic. For example, replace inline regex-based provider detection:

```js
// Bad: inline hardcoded routing logic
function resolveZedProvider(model) {
  if (/(claude|anthropic)/i.test(model)) return "anthropic";
  if (/(gemini|google)/i.test(model)) return "google";
  ...
}
```

with a config-driven lookup:

```js
// config/zedProviderPatterns.js
export const ZED_PROVIDER_PATTERNS = {
  anthropic: /(claude|anthropic)/i,
  google: /(gemini|google)/i,
  x_ai: /(grok|x[_-]?ai)/i,
};

// translator
import { ZED_PROVIDER_PATTERNS } from "../../config/zedProviderPatterns.js";
function resolveZedProvider(model) {
  for (const [provider, pattern] of Object.entries(ZED_PROVIDER_PATTERNS)) {
    if (pattern.test(model)) return provider;
  }
}
```

Applying this consistently prevents non-functional settings, unexpected implicit behavior, and scattered hardcoded config logic.