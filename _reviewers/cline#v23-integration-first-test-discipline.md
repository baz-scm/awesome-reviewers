---
title: Integration-First Test Discipline
description: 'Write tests that verify the real wiring/behavior while staying deterministic
  and isolated: (1) prefer adapter/wire-level tests when you’re validating request
  construction and integration boundaries—stub only the external IO (e.g., fetch),
  (2) keep unit tests focused and ensure they cannot hang or leak by stubbing the
  correct boundary (don’t rely on...'
repository: cline/cline#v23
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70889
---

Write tests that verify the real wiring/behavior while staying deterministic and isolated: (1) prefer adapter/wire-level tests when you’re validating request construction and integration boundaries—stub only the external IO (e.g., fetch), (2) keep unit tests focused and ensure they cannot hang or leak by stubbing the correct boundary (don’t rely on never-ending streams/listeners), (3) reuse exported constants/versions rather than duplicating strings in tests, (4) manage environment/external state with the test framework’s stubbing helpers and ensure proper cleanup, and (5) make assertions strict enough to prevent false positives (avoid permissive transformations that mask missing/incorrect spec data).

Example (wire-style integration with stubbed fetch + isolated env):
```ts
import { describe, it, expect, vi } from "vitest";

it("sends the real adapter request shape", async () => {
  const fetchStub = vi.fn(async (_url, req) => {
    return new Response(JSON.stringify({ text: "ok" }), { status: 200 });
  });
  vi.stubGlobal("fetch", fetchStub);

  // If your code reads env/config, use the framework’s env stub helpers:
  // vi.stubEnv({ CLINE_MCP_SETTINGS_PATH: tempPath });

  const result = await transcribeAudio({
    // use the real adapter config
  } as any);

  expect(fetchStub).toHaveBeenCalled();
  expect(result).toEqual(/* expected transcript */);

  vi.unstubAllGlobals();
  // vi.unstubAllEnvs(); // if you used stubEnv
});
```

Apply this as a team standard: when a test is meant to catch integration bugs, don’t over-mock internals; when it’s meant to be a unit test, don’t introduce brittle platform-specific plumbing or permissive logic that can pass with wrong behavior.