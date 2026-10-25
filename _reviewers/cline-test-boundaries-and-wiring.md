---
title: Test boundaries and wiring
description: 'When writing tests, choose the boundary intentionally: validate user-/system-relevant
  behavior without brittle low-level mocking, and stub only external dependencies.'
repository: CLINE/cline
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 70839
---

When writing tests, choose the boundary intentionally: validate user-/system-relevant behavior without brittle low-level mocking, and stub only external dependencies.

Practical rules:
- Prefer “real behavior” tests over mocking critical runtime plumbing (process spawning, log formats, etc.), especially when platform differences exist.
- If a bug happens in a multi-step state/render/wiring pipeline, don’t rely on helper-only/unit tests—test the composed behavior at the boundary where the bug manifests.
- For adapter/wiring coverage, run the real adapter code while stubbing external IO (e.g., network via fetch), then assert the request/response path.
- Stub at the correct abstraction layer to avoid hangs or leaked listeners (don’t feed never-ending streams if you can stub the terminal/process runner).
- Avoid brittle assertions on non-behavioral details (like exact log field payload shapes) when existing tests already exercise the behavioral path.
- Ensure tests enforce the actual correctness contract (e.g., don’t “flatten away” required plural categories; compare against the expected category sets).

Example pattern (adapter wiring):
```ts
it("wires request through the real adapter", async () => {
  const fetchStub = vi.fn(() => Promise.resolve(new Response(JSON.stringify({ text: "hi" }))));
  vi.stubGlobal("fetch", fetchStub);

  const result = await transcribeAudio({
    // real adapter used
    config: { type: "openai-native", model: "gpt-4o-mini-transcribe" },
    audio: /* ... */,
  });

  expect(fetchStub).toHaveBeenCalledWith(
    expect.stringContaining("/v1/audio/transcriptions"),
    expect.any(Object)
  );
  expect(result.text).toBe("hi");
});
```