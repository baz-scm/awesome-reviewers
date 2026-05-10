---
title: API Contract Verification
description: When adding/updating model-to-endpoint configuration, verify it against
  the provider’s official API docs and enforce the expected request/response contract.
repository: infiniflow/ragflow
label: API
language: Json
comments_count: 2
repository_stars: 80174
---

When adding/updating model-to-endpoint configuration, verify it against the provider’s official API docs and enforce the expected request/response contract.

Apply this standard:
1) Correct endpoint/path per model
- Don’t assume all models share the same URL suffix.
- Map each `model` to the exact endpoint/path described in the docs (e.g., rerank models may differ by provider).

2) Confirm response shape/schema compatibility
- Ensure your typed structs match the documented JSON fields (names, nesting, types).
- If the provider claims “OpenAI-compatible,” validate the key fields you depend on (e.g., `data[].index`, `data[].embedding`, `usage`, etc.).

3) Add defensive validations for upstream/proxy anomalies
- Validate lengths and indices before trusting arrays from responses.
- Reject or guard against duplicates, out-of-range indices, or count mismatches to prevent silent corruption.

Example pattern (Go-like pseudocode):
```go
// 1) Endpoint routing (per-model, docs-backed)
func urlSuffix(providerCfg map[string]string, model string) string {
  return providerCfg[model] // e.g., rerank models can have different suffixes
}

// 2) Defensive response validation
type EmbeddingData struct {
  Index     int
  Embedding []float64
  Object    string
}

type EmbeddingResponse struct {
  Data  []EmbeddingData
  Model string
  Object string
}

func normalizeEmbeddings(resp EmbeddingResponse, expectedCount int) ([][]float64, error) {
  if len(resp.Data) != expectedCount {
    return nil, fmt.Errorf("embedding count mismatch")
  }

  // Guard against duplicates/out-of-range
  seen := map[int]bool{}
  out := make([][]float64, expectedCount)
  for _, d := range resp.Data {
    if d.Index < 0 || d.Index >= expectedCount {
      return nil, fmt.Errorf("embedding index out of range")
    }
    if seen[d.Index] {
      return nil, fmt.Errorf("duplicate embedding index")
    }
    seen[d.Index] = true
    out[d.Index] = d.Embedding
  }
  return out, nil
}
```
Keep the docs link/source close to the mapping so future changes remain traceable and reviewable.