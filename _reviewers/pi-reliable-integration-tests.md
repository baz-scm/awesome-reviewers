---
title: Reliable integration tests
description: 'Integration/E2E tests should be structured and isolated: use consistent
  fixture setup/teardown to avoid flakiness and leftover files, and organize higher-level
  tests using reusable helpers and known-good inputs/models.'
repository: earendil-works/pi
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 79783
---

Integration/E2E tests should be structured and isolated: use consistent fixture setup/teardown to avoid flakiness and leftover files, and organize higher-level tests using reusable helpers and known-good inputs/models.

Apply this standard:
- Fixtures/cleanup: create temp directories/files using OS-safe helpers (e.g., mkdtempSync or mkdtemp), and always clean them in afterEach with rmSync(tempDir, { recursive: true, force: true }). Avoid ad-hoc temp naming (e.g., Date.now-based dirs) unless necessary.
- Test levels/structure:
  - Add an end-to-end test where the behavior depends on external systems.
  - Follow existing test templates in the repo.
  - Organize tests by capability/provider (one describe per provider) and call shared helper functions for provider-specific subtests using a known-good model/input.

Example (fixture + cleanup):
```ts
import { afterEach, describe, it, expect } from "vitest";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

describe("some integration", () => {
  let tempDir: string;

  beforeEach(() => {
    tempDir = mkdtempSync(join(tmpdir(), "pi-test-"));
  });

  afterEach(() => {
    rmSync(tempDir, { recursive: true, force: true });
  });

  it("does the thing", () => {
    // use tempDir safely
    expect(tempDir).toBeTruthy();
  });
});
```

Example (provider-organized E2E/unit structure sketch):
```ts
describe("openrouter provider", () => {
  const knownGoodModel = "<provider-specific model>";

  // shared helper used by multiple subtests
  const runProviderTest = (input: unknown) => {/* call provider with knownGoodModel */};

  it("does X", async () => {
    const result = await runProviderTest({/* ... */});
    // assert
  });
});
```