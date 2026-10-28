---
title: Verified, scoped config changes
description: Configuration entries (detection manifests, feature flags, dependency
  features, etc.) must be backed by concrete, verified evidence rather than assumption.
  Before adding a rule or flag, confirm it against an actual observed capture or documented
  behavior; don't add speculative entries "just in case" — e.g., a footer-only trust-dialog
  rule was rejected...
repository: ogulcancelik/herdr#canary966c66ad
label: Configurations
language: Toml
comments_count: 3
repository_stars: 46332
---

Configuration entries (detection manifests, feature flags, dependency features, etc.) must be backed by concrete, verified evidence rather than assumption. Before adding a rule or flag, confirm it against an actual observed capture or documented behavior; don't add speculative entries "just in case" — e.g., a footer-only trust-dialog rule was rejected because no capture actually showed that pattern, and would have collided with an existing rule anyway.

When a config file documents evidence in comments (e.g., captured footer strings, UI states), the implemented rule/pattern must fully cover every variant called out in that evidence — audit new rules against their own documentation before merging, as in the case where `/theme`'s `enter save` footer was documented but missing from the actual `any = [...]` match list, silently falling through to the wrong state. When fixing such a gap, update every related gate (e.g., not-gates that must stay in sync with the rule they exclude) and every mirrored copy of the config (e.g., manifest plus its website duplicate) together, and re-run the manifest/consistency checks to confirm.

Additionally, scope configuration and feature-flag changes as narrowly as possible to limit blast radius. Prefer a local, targeted dependency or setting over flipping a shared/global feature flag whose side effects ripple across unrelated subsystems. For example, add a direct `indexmap` dependency with `serde` support instead of enabling `serde_json/preserve_order`, which would silently change map ordering across the entire API and persistence layer rather than just the one feature being changed.