---
title: Scoped Provider Transformations
description: 'When implementing AI/LLM request transformers (especially for proxies),
  make provider-specific shaping:


  1) **Scoped and structured**: Clone the incoming `llm.Request` and apply provider/CLI-specific
  changes via existing structured fields **before** delegating to the shared/base
  transformer whenever possible. Avoid raw `[]byte` request-body manipulation...'
repository: looplj/axonhub
label: AI
language: Go
comments_count: 2
repository_stars: 4808
---

When implementing AI/LLM request transformers (especially for proxies), make provider-specific shaping:

1) **Scoped and structured**: Clone the incoming `llm.Request` and apply provider/CLI-specific changes via existing structured fields **before** delegating to the shared/base transformer whenever possible. Avoid raw `[]byte` request-body manipulation unless the field truly can’t be represented structurally.

2) **No shared-model pollution**: If a change (e.g., tool-name prefixing) would break assumptions for other transformers, ensure the change is applied only within the cloned request or handled by the provider-specific transformer layer.

3) **Idempotent system prompt injection**: If your proxy adds a provider system message (e.g., Claude Code), first detect whether the request already contains that system prompt (or any system prompt) to prevent duplicates.

Example (idempotent system injection + scoped preprocessing):
```go
func (t *ClaudeCodeTransformer) TransformRequest(ctx context.Context, llmReq *llm.Request) (*httpclient.Request, error) {
	if llmReq == nil { return nil, fmt.Errorf("request is nil") }

	// Always work on a copy to avoid cross-request/state issues.
	reqCopy := *llmReq

	// 1) Idempotent system message injection.
	const sys = "You are Claude Code, Anthropic's official CLI for Claude."
	if !hasSystemPrompt(reqCopy.Messages, sys) {
		systemMsg := llm.Message{
			Role: "system",
			Content: llm.MessageContent{Content: lo.ToPtr(sys)},
		}
		reqCopy.Messages = append([]llm.Message{systemMsg}, reqCopy.Messages...)
	}

	// 2) Provider-specific structured preprocessing (only what the model supports).
	// Apply tool prefixing / cache control / metadata shaping only to reqCopy,
	// and keep other transformers unaffected.
	applyClaudeToolPrefix(&reqCopy)
	// (If a needed field is not representable structurally, then do minimal byte surgery later.)

	return t.Outbound.TransformRequest(ctx, &reqCopy)
}

func hasSystemPrompt(msgs []llm.Message, sys string) bool {
	for _, m := range msgs {
		if m.Role == "system" && m.Content.Content != nil && *m.Content.Content == sys {
			return true
		}
	}
	return false
}
```
Adopting these rules improves **correctness** (no duplicated system instructions), **maintainability** (less brittle byte-level edits), and **compatibility** (provider specifics don’t unintentionally affect other LLM transformers).