---
title: Integration-first Testing Strategy
description: 'When writing tests, prefer realistic, behavior-focused coverage and
  strong isolation—avoid brittle harnesses and brittle assertions.


  **Guidelines**

  1. **Use wire/integration tests for adapter/runtime wiring.** If unit mocks can’t
  exercise the real adapter integration (e.g., type-cast mismatch, request path wiring),
  add a test that drives the real adapter...'
repository: cline/cline#v29
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 70893
---

When writing tests, prefer realistic, behavior-focused coverage and strong isolation—avoid brittle harnesses and brittle assertions.

**Guidelines**
1. **Use wire/integration tests for adapter/runtime wiring.** If unit mocks can’t exercise the real adapter integration (e.g., type-cast mismatch, request path wiring), add a test that drives the real adapter with only the external boundary stubbed.
2. **Don’t add test-only plumbing that breaks cross-platform behavior.** If correct verification depends on real processes/tools, validate via real CLI/VS Code sessions or other environment-appropriate integration.
3. **Isolate and clean up all external side effects.**
   - Stub env vars with the test framework’s env utilities and fully restore afterwards.
   - Use temp directories and isolated discovery/config paths so tests can’t touch a developer’s real state.
   - Stub the correct system/prototype entrypoints so no long-lived streams/listeners outlive the test.
4. **Assert behavior, not incidental implementation details.** Prefer assertions on outcomes and protocol/requests over log payload field-name shapes.
5. **For state machines/sequences, add invariants + fuzz/regression.** Combine deterministic regression sequences with lightweight fuzz/property checks to cover unexpected verb orderings.

**Example pattern (isolation + real behavior, with minimal stubbing)**
```ts
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { vi } from 'vitest';

it('runs the real adapter with isolated environment', async () => {
  const home = mkdtempSync(join(tmpdir(), 'smoke-'));

  vi.stubEnv('HOME', home);
  vi.stubEnv('CLINE_DATA_DIR', join(home, 'data'));
  vi.stubEnv('CLINE_HUB_DISCOVERY_PATH', join(home, 'discovery.json'));

  // Stub only the external boundary (e.g., fetch) if needed.
  vi.stubGlobal('fetch', async () => new Response(/* ... */));

  // Drive behavior through the real adapter/module.
  const res = await transcribeAudio(/* real config */);
  expect(res).toMatchObject({ /* expected behavior */ });

  vi.unstubAllEnvs();
});
```

Applying these rules will reduce flaky tests, improve bug detection in runtime integration points, and keep the suite resilient to unrelated implementation changes.