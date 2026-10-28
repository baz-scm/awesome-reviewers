---
title: Semantic naming accuracy
description: Choose names that precisely match what a variable, parameter, or function
  actually computes or does — not a narrower, vaguer, or inverted description of it.
  If reading the code reveals the name is testing something broader/different than
  it implies, rename it so the usage site reads naturally as the test it performs
  (e.g. a boolean that also accounts for...
repository: "cline/cline\r\n"
label: Naming Conventions
language: TypeScript
comments_count: 4
repository_stars: 70946
---

Choose names that precisely match what a variable, parameter, or function actually computes or does — not a narrower, vaguer, or inverted description of it. If reading the code reveals the name is testing something broader/different than it implies, rename it so the usage site reads naturally as the test it performs (e.g. a boolean that also accounts for "still preparing" state should be named `sessionIdle`, not the narrower `canStartRun`; a flag that's immediately negated and whose meaning is unclear, like `background`, should be renamed to what it actually represents, e.g. `userInitiated`).

When two or more exported functions/types serve overlapping purposes, don't leave callers to guess which one to use from the names alone. Prefer exposing a single canonical public entry point (keep helpers private, or export them only for testing via an explicit, clearly-labeled mechanism). If multiple public APIs are truly necessary, give them names that strongly hint at when each should be used, backed by thorough doc comments that remove any ambiguity — e.g. `findUsableFallbackProviderId` and `resolveEffectiveLastUsedProviderId` need either a single wrapper or much stronger differentiating names/docs.

Also keep naming consistent for the same concept across packages/modules — avoid introducing a new type (e.g. `ClinePrivacySettingsClient`) when an existing shared type (e.g. `ClientName`) already models the same concept; extend the existing type instead of duplicating it under a different name.