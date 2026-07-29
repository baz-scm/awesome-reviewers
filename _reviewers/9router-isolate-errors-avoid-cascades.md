---
title: Isolate errors, avoid cascades
description: When a feature depends on multiple probes/loads, ensure that failures
  in secondary/best-effort steps don’t corrupt primary state or cause cascading failures.
repository: decolua/9router
label: Error Handling
language: JavaScript
comments_count: 2
repository_stars: 23951
---

When a feature depends on multiple probes/loads, ensure that failures in secondary/best-effort steps don’t corrupt primary state or cause cascading failures.

Apply this in two ways:
1) Runtime/state handling: keep authoritative flags separate from enrichment fields.
   - Compute primary status from the most reliable probe (e.g., a CLI “installed” check).
   - Treat secondary lookups (e.g., `pip list`, optional extras) as best-effort: on failure, return safe defaults for only the enrichment fields, not the primary flag.

   Example pattern:
   ```js
   export async function getStatus(url) {
     const installed = Boolean(pathFromCliProbe);

     // Best-effort enrichment; should NOT affect `installed`.
     let extras = { version: null, extras: { code: false, ml: false } };
     try {
       if (installed) extras = await getInstalledHeadroomExtras();
     } catch {
       // swallow or log; keep primary state stable
     }

     return { installed, ...extras };
   }
   ```

2) Test structure: fail fast in setup.
   - Load/import prerequisites in a `before()`/setup hook.
   - If loading fails, the test should fail once at setup and not continue with `undefined` values that produce many misleading downstream errors.

   Example pattern:
   ```js
   import { before, it } from "node:test";
   import assert from "node:assert/strict";

   let entry;
   before(async () => {
     entry = (await import("../../path/to/module.js")).default;
   });

   it("has expected id", () => {
     assert.equal(entry.id, "kimchi");
   });
   ```

This prevents both incorrect UI/business logic (wrong state derived from a failing secondary probe) and noisy, cascading test failures that obscure the real cause.