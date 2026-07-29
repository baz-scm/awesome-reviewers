---
title: Semantic Naming Consistency
description: 'Adopt naming rules that accurately reflect meaning, routing behavior,
  and established codebase conventions.


  Apply these checks when adding/changing code:'
repository: maximhq/bifrost
label: Naming Conventions
language: Go
comments_count: 6
repository_stars: 6862
---

Adopt naming rules that accurately reflect meaning, routing behavior, and established codebase conventions.

Apply these checks when adding/changing code:
- Provider-specific vs provider-agnostic naming: If a helper operates on shared Bifrost schema types (e.g., `BifrostResponsesResponse`) and isn’t actually OpenAI-specific, avoid placing it in `openai/*` and avoid OpenAI-specific naming; move it to provider-agnostic utils and name it for the shared concept.
- Follow existing file/type conventions: For non-OpenAI providers, define the provider struct in the main `<name>.go` file, and reserve `types.go` for provider-specific request/response DTO structs.
- Use the correct semantic field: Prefer the modern/non-deprecated field for provider attribution (e.g., routing/provider information) and ensure call sites use the populated source that matches the pipeline.
- Align sentinel names/docs with config: If you use a “disabled” sentinel, name it explicitly (e.g., `LiveModelsSyncDisabled`) and ensure docs and schema/config describe the same disable value semantics.
- Preserve identifier semantics: When building compound IDs used for routing, parse and detect already-present inference-provider/policy segments; don’t blindly prepend segments (prepending twice breaks routing).
- Type naming consistency: Name new types to match existing conventions (e.g., include the relevant parent/type prefix like `ChatAssistantMessageImage` for assistant-message image entries).

Example (compound ID duplication guard):
```go
first, modelOrName, found := strings.Cut(rawID, "/")
if found && isKnownInferenceProviderOrPolicy(first) {
	// rawID already includes an inference-provider/policy segment; do not prepend again
} else {
	// safe to prepend providerKey/inferenceProvider
	m.ID = fmt.Sprintf("%s/%s/%s", providerKey, inferenceProvider, rawID)
}
_ = modelOrName
```