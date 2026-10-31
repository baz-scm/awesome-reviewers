---
title: Pin provider wire contracts
description: 'LLM providers and even individual model ids within a provider diverge
  in what they accept and report: tool-schema shape requirements (e.g. Gemini needs
  an explicit `type: "object"` root, nested `items`/`anyOf`/`oneOf`/`allOf` need the
  same casing/normalization as the top level), which reasoning settings a model can
  take (`effort: "none"` is valid for some...'
repository: cline/cline?foo=bar
label: AI
language: TypeScript
comments_count: 8
repository_stars: 71082
---

LLM providers and even individual model ids within a provider diverge in what they accept and report: tool-schema shape requirements (e.g. Gemini needs an explicit `type: "object"` root, nested `items`/`anyOf`/`oneOf`/`allOf` need the same casing/normalization as the top level), which reasoning settings a model can take (`effort: "none"` is valid for some ids but rejected by others), how usage/token counts are nested (reasoning tokens show up under different paths depending on SDK version and must be reconciled, not double-counted), how retries and timeouts interact with streaming (don't assume an error is retryable or that a slow-to-stream reasoning model has stalled), and how model ids get resolved/rewritten by internal catalogs (e.g. a bare model id silently becomes a region-qualified profile id). Because these quirks are per-model and often invisible from our own wrapper code, cover them with wire-contract tests that exercise the *real* adapter with a stubbed `fetch`/HTTP layer and assert on the actual outgoing request (or parsed response) body, parameterized per model id/capability rather than asserted generically. When a quirk is really a bug in the underlying adapter/SDK (e.g. Bedrock's reasoning handling), prefer fixing or special-casing it as narrowly as possible, document why, and consider upstreaming the fix rather than growing provider-specific branches in shared code.

Example pattern to follow:
```ts
async function wireBody(input: { modelId: string; reasoning?: ReasoningOption }) {
  let body: Record<string, unknown> | undefined;
  const fetchStub = (async (_input, init) => {
    body = JSON.parse((init?.body as string) ?? "{}");
    return new Response(JSON.stringify({ error: { message: "stub" } }), { status: 400 });
  }) as typeof fetch;

  const gateway = createGateway({ providerConfigs: [{ providerId: "openai-native", fetch: fetchStub }] });
  for await (const _ of await gateway.stream({ modelId: input.modelId, reasoning: input.reasoning, messages: [...] })) {}
  return body!;
}

it("does not send effort:none to a model that cannot turn reasoning off", async () => {
  const body = await wireBody({ modelId: "gpt-6-astra", reasoning: { enabled: false } });
  expect((body.reasoning as { effort?: string })?.effort).not.toBe("none");
});
```
This catches regressions that unit tests against our own normalization logic would miss, since the bug is in how a specific model/adapter combination maps onto the wire protocol.