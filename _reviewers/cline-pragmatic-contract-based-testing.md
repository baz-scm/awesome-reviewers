---
title: Pragmatic, contract-based testing
description: 'When adding/updating tests, optimize for stable, cross-platform correctness
  and isolation:


  - **Assert behavior and contracts, not implementation noise.** Prefer correctness
  checks already exercised by existing suites over brittle assertions on internal
  payload shapes (e.g., exact log field structures), unless that structure is the
  behavior users rely on.'
repository: CLINE/CLINE
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70837
---

When adding/updating tests, optimize for stable, cross-platform correctness and isolation:

- **Assert behavior and contracts, not implementation noise.** Prefer correctness checks already exercised by existing suites over brittle assertions on internal payload shapes (e.g., exact log field structures), unless that structure is the behavior users rely on.
- **Use shared source-of-truth constants.** Don’t hardcode package/version strings in tests; import the exported constant and add a dedicated test to ensure it matches the authoritative source (e.g., the core package’s `package.json`).
- **Keep tests non-leaky.** Stub the right layer to prevent never-ending streams, long-running promises, or event listeners from surviving past the test.
- **Use framework-native env/mocking helpers.** Restore environment state with the matching helper APIs (so tests behave correctly whether variables were originally set or unset).
- **Make assertions strict enough to prevent false positives.** If required data must cover specific groups/categories (e.g., CLDR plural cardinal categories), ensure tests fail when any required group is missing—not just when the happy-path keys exist.

Example (pattern):
```ts
import { SKILLS_CLI_PACKAGE } from "@cline/core";
import { describe, expect, it, vi } from "vitest";

it("builds args using exported constants", () => {
  expect(buildSkillsArgs(["list"]))
    .toEqual(["-y", SKILLS_CLI_PACKAGE, "list"]);
});

describe("env-dependent command", () => {
  it("writes config using stubbed env", async () => {
    vi.stubEnv({ CLINE_MCP_SETTINGS_PATH: "/tmp/settings.json" });
    try {
      const code = await runMcpInstallCommand(/* ... */);
      expect(code).toBe(0);
    } finally {
      vi.unstubAllEnvs();
    }
  });
});
```

Apply this as a quick checklist for every test change: **(1) contract-based assertions, (2) strict correctness coverage, (3) no leaks, (4) safe env/mocking, (5) avoid brittle internals.**