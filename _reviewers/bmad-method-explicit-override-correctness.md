---
title: Explicit override correctness
description: When handling configuration from CLI/UI (e.g., `--set`, channel flags,
  migration prompts), treat user-provided values as explicit assertions that must
  (a) be seeded into the same data pipeline that prompts/templates use, (b) survive
  any schema-strict filtering only because the user asserted them, and (c) not be
  overwritten later by default/template/prompt...
repository: bmad-code-org/bmad-method
label: Configurations
language: JavaScript
comments_count: 6
repository_stars: 51859
---

When handling configuration from CLI/UI (e.g., `--set`, channel flags, migration prompts), treat user-provided values as explicit assertions that must (a) be seeded into the same data pipeline that prompts/templates use, (b) survive any schema-strict filtering only because the user asserted them, and (c) not be overwritten later by default/template/prompt logic.

Apply this checklist:
- Seed overrides *before* prompt/result processing so both interactive and `--yes`/skip paths see them as already-set.
- For overrides on unknown keys: warn, persist them, but ensure they’re not mistakenly treated as schema-declared.
- Preserve schema-strict behavior: keep undeclared keys only if they were explicitly asserted (tracked via an override-key set), not merely because they appear in intermediate answered config.
- Respect schema entry types: if a key is declared as `result` (no `prompt`), allow overrides to flow through the result-template rendering (don’t warn as “unknown” or stomp raw values).
- In update/upgrade flows with channels: add an “alreadyDecided”/intent guard so explicit flags (`--pin`, `--next`, `--channel`) skip upgrade/prompt logic and aren’t overwritten by recorded manifest state.
- Avoid brittle config constants: don’t hardcode config paths (use shared/base values like `this.bmadFolderName`), and don’t set runtime-breaking env options (e.g., invalid `NODE_OPTIONS` flags for the supported Node version).

Example pattern (seeding + filtering prompts):
```js
const declaredKeys = new Set(configKeysFromSchema(itemOrModule));
const overrides = cliOverrides[moduleName] ?? {};
const seededKeys = new Set();
const unknown = [];
for (const [k,v] of Object.entries(overrides)) {
  if (declaredKeys.has(k)) seededKeys.add(k);
  else unknown.push(k);
}

// Seed answers so prompt/template/default logic won’t overwrite.
let allAnswers = { ...staticAnswers };
for (const k of seededKeys) allAnswers[`${moduleName}_${k}`] = overrides[k];

// Remove corresponding questions so interactive flow doesn’t reprompt.
questions = questions.filter(q => !seededKeys.has(q.name.replace(`${moduleName}_`, '')));

// Track seededKeys so schema-strict partition keeps them.
setOverrideKeys[moduleName] = [...(setOverrideKeys[moduleName] ?? []), ...seededKeys];
```
