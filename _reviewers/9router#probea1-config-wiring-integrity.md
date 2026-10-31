---
title: Config wiring integrity
description: 'When introducing or modifying configuration (env vars, settings, feature
  flags, generated registries), ensure the full read/write path is consistent, validated,
  and safe by default:'
repository: decolua/9router#probeA1
label: Configurations
language: JavaScript
comments_count: 4
repository_stars: 31730
---

When introducing or modifying configuration (env vars, settings, feature flags, generated registries), ensure the full read/write path is consistent, validated, and safe by default:

1. Don't add "dead" knobs. If code reads a setting (e.g. `providerOverrides.timeoutMs`), confirm there is an actual write path that persists it (e.g. the API route's normalizer) and that it validates the value (finite, within sane min/max bounds). If the write path doesn't support it yet, either extend it or remove the read so you don't advertise a setting that silently can't be saved.
2. Respect externally supplied environment variables rather than clobbering them. Build/launch scripts should check if a variable (e.g. `NEXT_DIST_DIR`, `NEXT_TRACING_ROOT_MODE`) is already set by the caller and short-circuit instead of overwriting it.
3. Unset/empty config should default to the safest, most explicit state — don't let an empty setting silently trigger implicit fallback logic (e.g. auto-picking a provider when `webSearchFallbackProvider` is unset). If a feature is documented as "off until configured," an unset value must produce a clear declined/disabled result, not a best-guess substitute.
4. Never hand-edit generated configuration/wiring files (e.g. `registry/index.js`). Use the provided generation script (e.g. `scripts/migrate-registry.mjs`) so the auto-generated list stays consistent with its source files.

Following these practices prevents configuration options that look functional but aren't actually honored, avoids clobbering caller-provided environment, and keeps feature flags predictable and auto-generated files trustworthy.