---
title: Centralize and validate configuration
description: All configurable values—provider overrides, environment variables, feature
  flags, routing patterns, etc.—must flow consistently through a single, validated
  configuration layer rather than being hardcoded, silently dropped, or clobbered.
repository: decolua/9router#;sleep 4
label: Configurations
language: JavaScript
comments_count: 3
repository_stars: 31756
---

All configurable values—provider overrides, environment variables, feature flags, routing patterns, etc.—must flow consistently through a single, validated configuration layer rather than being hardcoded, silently dropped, or clobbered.

- Never hardcode values, model names, or role/block strings directly in business logic; move them into `config/` or `schema/` constants so they can be audited and reused. For example, instead of inlining a regex map in a translator, define it in the provider's config module:
  ```js
  // config/zedProviderPatterns.js
  export const ZED_PROVIDER_PATTERNS = {
    anthropic: /(claude|anthropic)/i,
    google: /(gemini|google)/i,
    x_ai: /(grok|x[_-]?ai)/i,
  };
  ```
  and reference `ZED_PROVIDER_PATTERNS` from the translator.

- If code reads a configuration field (e.g. `providerOverrides.timeoutMs` or `seatBudgetMs`), ensure the corresponding write path (API routes, normalization/validation functions) actually supports and validates that field (finite, within bounds, etc.). Don't leave "ghost" settings that can only be set by manually editing the database—either wire up full validation end-to-end or remove the unused read path so the code doesn't advertise a setting that can't actually be configured.

- When scripts or build tooling set environment variables, check for and respect any caller-provided values first (e.g. `NEXT_DIST_DIR`, `NEXT_TRACING_ROOT_MODE`) instead of unconditionally overwriting them, to avoid breaking downstream sandboxing/tracing behavior.

Applying this standard keeps configuration discoverable, consistent, and safe to change, and prevents silent gaps between what the code reads and what the system actually allows users to configure.</description>
</invoke>
