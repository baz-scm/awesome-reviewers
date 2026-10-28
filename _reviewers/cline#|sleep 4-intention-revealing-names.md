---
title: Intention-revealing names
description: 'Choose identifier names that describe what something *is* or *does*,
  not names that only make sense once negated or require the reader to infer meaning
  from usage. Avoid boolean flags for non-binary domains; prefer a descriptive string/enum
  that names each state positively (e.g. `entry: "run" | "continue"` instead of a
  `continueRun: boolean`, or...'
repository: cline/cline#|sleep 4
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 70979
---

Choose identifier names that describe what something *is* or *does*, not names that only make sense once negated or require the reader to infer meaning from usage. Avoid boolean flags for non-binary domains; prefer a descriptive string/enum that names each state positively (e.g. `entry: "run" | "continue"` instead of a `continueRun: boolean`, or `promptSeeded?: "seeded" | "written"` style states instead of an opaque flag). When a parameter or field reads naturally only through negation (e.g. `background` used as `!background`), rename it to the concept it actually represents (e.g. `userInitiated`).

When two or more exported functions/types serve overlapping purposes (e.g. `findUsableFallbackProviderId` vs `resolveEffectiveLastUsedProviderId`, or a locally duplicated `ClinePrivacySettingsClient` vs the shared `ClientName`), either collapse them into a single public entry point with internal helpers exposed only for testing, or give each a name that strongly signals when to use it, backed by a precise doc comment that removes any doubt. Prefer reusing an existing shared type/enum over introducing a near-duplicate with a different name for the same concept.

Keep naming/casing consistent with the convention already established for that context rather than introducing a one-off style — e.g., if camelCase is used for caller-supplied keys and snake_case for system/envelope-added keys, a new key should follow whichever convention matches its origin, not the convention of unrelated neighboring keys. Also prefer naming async accessors as the value they resolve to when that reads more naturally at call sites (e.g. a cached promise field `turnAccepted` instead of a `whenTurnAccepted()` method), so usage like `await turnAccepted` stays idiomatic.