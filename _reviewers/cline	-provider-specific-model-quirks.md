---
title: Provider-specific model quirks
description: 'LLM providers and models disagree on fundamentals that code must not
  paper over with a single shared assumption: whether reasoning tokens are counted
  inside or outside `outputTokens`, whether a catalog''s advertised context length
  is actually what a locally loaded model will serve (vs. its ceiling), whether a
  given model id can turn reasoning off at all,...'
repository: "cline/cline\t"
label: AI
language: TypeScript
comments_count: 7
repository_stars: 70947
---

LLM providers and models disagree on fundamentals that code must not paper over with a single shared assumption: whether reasoning tokens are counted inside or outside `outputTokens`, whether a catalog's advertised context length is actually what a locally loaded model will serve (vs. its ceiling), whether a given model id can turn reasoning off at all, what retry/backoff semantics an adapter actually performs versus what its docs claim, and how long a model may legitimately sit silent before its first visible token. Treat every such behavior as provider- and model-specific rather than universal: branch on it explicitly, document the provider quirk being handled in a comment, and prefer runtime-reported values (e.g. a model's `loaded_context_length`) over static catalog ceilings when both exist.

Because these quirks are easy to get wrong and easy to silently regress, pin them with wire-contract tests that exercise the *real* SDK adapter (stubbed only at the HTTP boundary), not a hand-rolled mock of its behavior — a mock can't catch a change in the adapter's own translation logic. Each test should state which regression it guards and over which model ids/providers, so a future catalog or adapter bump that reintroduces the issue fails loudly. When a test's assertion would only pin the adapter's own internal classification (nothing routed through our code), that belongs in the adapter's own test suite, not ours — keep assertions scoped to what our resolver/catalog/routing actually controls.

Example of the pattern to follow:
```ts
// Bedrock: models the adapter cannot classify must get no reasoning fields at
// all, not a reasoningConfig Bedrock rejects for non-reasoning models
// (cline/cline#14095). Pinned against the real @ai-sdk/amazon-bedrock adapter.
it("sends no reasoning fields for an unclassified model", async () => {
  const fields = await additionalModelRequestFields("some.unlisted-model");
  expect(fields).toBeNull();
});
```