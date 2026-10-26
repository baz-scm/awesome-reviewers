---
title: Semantic Naming Rules
description: 'Adopt naming that encodes *meaning*, stays consistent with shared contracts,
  and prevents accidental semantic drift.


  **Rules**

  1. **Prefer semantic names over vague flags**'
repository: cline/cline#v7
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70865
---

Adopt naming that encodes *meaning*, stays consistent with shared contracts, and prevents accidental semantic drift.

**Rules**
1. **Prefer semantic names over vague flags**
   - Avoid boolean flags whose semantics are unclear or require double-negation.
   - Prefer positive, intent-revealing names (and consider renaming to describe user/action origin).

   ```ts
   // Prefer
   load(refresh: boolean, userInitiated = false)

   // Over
   load(refresh: boolean, background = false) // if callers immediately negate
   ```

2. **If the domain isn’t truly boolean, don’t use booleans**
   - When “true/false” is really “state A/state B”, use a small string enum.

   ```ts
   entry?: 'run' | 'continue';
   promptSeeded?: 'seeded' | 'written'; // instead of a boolean like `isSeeded`
   ```

3. **Align with shared types/contracts**
   - Reuse the project’s canonical identifier unions/types (e.g., shared `ClientName`) instead of ad-hoc strings.
   - If a host/client exists in practice but isn’t in the type, extend the type to match reality.

4. **Keep telemetry/event property keys stable and semantically correct**
   - If you rename a parameter/property (e.g., `taskId` → `ulid`), update *all* call sites and ensure every event writes the same identifier format under the same key.
   - Avoid positional-renaming pitfalls where TypeScript can’t catch semantic mismatches.

5. **Follow existing casing conventions based on origin**
   - Use the codebase convention: caller-supplied `context` keys as camelCase; envelope/global enrichment keys as snake_case (or whatever the established split is in your repo). Don’t “fix” one key’s casing if it changes the implied source.

6. **Make exported API names help callers choose**
   - Public function/type names should strongly hint intent and which one to call.
   - If multiple public functions are easy to misuse, prefer a single obvious entry point or add unmistakable naming.

7. **Eliminate magic values in favor of named constants**
   - Extract hard-coded timeouts/delays into named constants and document what the grace period is for.

   ```ts
   const OUTPUT_DRAIN_GRACE_PERIOD_MS = 1_000;
   setTimeout(() => { /* settle after draining */ }, OUTPUT_DRAIN_GRACE_PERIOD_MS);
   ```

Apply this whenever you introduce or rename: variable names, flags, exported functions, telemetry property keys, and cross-system identifiers.