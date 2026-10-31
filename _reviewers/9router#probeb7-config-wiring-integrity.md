---
title: Config wiring integrity
description: 'Treat configuration as a single consistent pipeline: every value you
  read somewhere must have a real, validated way to be written, and every routing/business
  constant must live in config, not inline code.'
repository: decolua/9router#probeB7
label: Configurations
language: JavaScript
comments_count: 3
repository_stars: 31737
---

Treat configuration as a single consistent pipeline: every value you read somewhere must have a real, validated way to be written, and every routing/business constant must live in config, not inline code.

1. End-to-end wiring: before reading a new setting (e.g. `providerOverrides.timeoutMs`), confirm the write path actually persists it with proper validation (type, bounds, defaults). If `normalizeOverride`-style sanitizers strip a field, either extend them to accept and validate it, or remove the dead read path. Don't ship a "knob" that only works via manual DB edits.

2. No hardcoded routing/model logic: provider/model detection rules, block/role strings, and similar literals must be defined in `config/` (or `schema/`) constants, not embedded as inline regexes or string literals in translators/handlers.
   ```js
   // Bad: inline, hardcoded in translator
   if (/(claude|anthropic)/i.test(model)) return "anthropic";

   // Good: centralized config
   // config/zedProviderPatterns.js
   export const ZED_PROVIDER_PATTERNS = {
     anthropic: /(claude|anthropic)/i,
     google: /(gemini|google)/i,
     x_ai: /(grok|x[_-]?ai)/i,
   };
   ```

3. Respect generated config artifacts: files marked as auto-generated (e.g. `registry/index.js`) must never be hand-edited. Add new entries by running the designated generation script (e.g. `scripts/migrate-registry.mjs`) so the artifact stays consistent with its source of truth.

Applying these checks prevents silently broken settings, scattered magic values, and drift in generated configuration files.