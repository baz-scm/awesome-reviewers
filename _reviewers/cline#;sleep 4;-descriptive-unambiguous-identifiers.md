---
title: Descriptive, unambiguous identifiers
description: 'Choose names that describe what a value *is* or *means*, not how it
  happens to be checked or where it came from incidentally. Concretely:


  - Avoid vague or negation-based booleans. If a parameter is only ever read as `!flag`,
  or its name doesn''t say what "true"/"false" actually mean, rename it to describe
  the positive state directly (e.g. `background` →...'
repository: cline/cline#;sleep 4;
label: Naming Conventions
language: TypeScript
comments_count: 4
repository_stars: 70976
---

Choose names that describe what a value *is* or *means*, not how it happens to be checked or where it came from incidentally. Concretely:

- Avoid vague or negation-based booleans. If a parameter is only ever read as `!flag`, or its name doesn't say what "true"/"false" actually mean, rename it to describe the positive state directly (e.g. `background` → `userInitiated`, so call sites read naturally as `if (userInitiated)`).
- When a flag's domain has more than one real state, don't force it into a boolean — model it as a small string union/enum whose values are self-explanatory (`entry?: "seeded" | "written"` is clearer than `promptSeeded?: boolean`, since it also names the "false" case instead of leaving it implicit).
- When exposing multiple public functions that look similar but solve different problems, don't rely on subtly different names to tell them apart (e.g. `findUsableFallbackProviderId` vs `resolveEffectiveLastUsedProviderId`). Prefer exporting a single, obviously-correct entry point and keep the alternative internal (or only exposed for testing); if both truly must be public, give them names and doc comments that make the decision of "which one do I call" unambiguous at the call site.
- Keep casing/naming conventions consistent with the semantic origin of the data, not just visual similarity to neighboring keys. For example, in telemetry payloads, caller-supplied context keys use camelCase (`runId`, `modelId`, `finishReason`) while envelope/global-enrichment keys use snake_case (`error_message`, `distinct_id`); match the convention for where a key is produced, not for where it happens to be read.

Before merging, ask: does this name tell a new reader what the value represents without needing to read the implementation, and does it avoid colliding semantically with another exported name nearby?