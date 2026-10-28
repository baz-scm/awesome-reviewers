---
title: Name by intent
description: Choose identifiers that describe what a value represents or what a function
  is actually for, not the mechanism used to compute it or a vague placeholder term.
  Before naming, ask "what does this test/value mean to the reader?" rather than "how
  was it derived?". For example, a boolean parameter named `background` that is only
  ever used as `!background` should...
repository: cline/cline#&&sleep 4
label: Naming Conventions
language: TypeScript
comments_count: 4
repository_stars: 70980
---

Choose identifiers that describe what a value represents or what a function is actually for, not the mechanism used to compute it or a vague placeholder term. Before naming, ask "what does this test/value mean to the reader?" rather than "how was it derived?". For example, a boolean parameter named `background` that is only ever used as `!background` should instead be `userInitiated`, and a variable assigned `!this.hasActiveTurn(session)` should be named for the broader condition it actually represents (e.g. `sessionIdle`) rather than reusing a narrower helper's name.

When multiple public functions have overlapping purposes and similar names (e.g. `findUsableFallbackProviderId` vs. `resolveEffectiveLastUsedProviderId`), do not leave callers to guess which one to use. Prefer exposing a single canonical entry point and keep helper functions private/internal (export them only for testing, and make that intent explicit); if several variants must stay public, give them names and doc comments that make the correct choice obvious at the call site.

Keep naming/casing conventions consistent with established, meaning-based rules already in the codebase rather than inventing new ones ad hoc — e.g. telemetry keys use camelCase when supplied by the call site and snake_case when added by the envelope/global enrichment, so a new context key should follow the convention for where it originates, not merely match nearby keys. When renaming a parameter or property, grep and update every call site (and any positional-argument usages) in the same change, since a silent rename can compile but change the meaning of the data being recorded or passed downstream.</description>
</invoke>
