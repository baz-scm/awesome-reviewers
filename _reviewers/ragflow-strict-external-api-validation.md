---
title: Strict External API Validation
description: When integrating with external AI/HTTP APIs, treat both transport errors
  and payload validity as first-class failures. Validate inputs, verify provider/HTTP
  status, and enforce response invariants—never silently accept partial or malformed
  data.
repository: infiniflow/ragflow
label: Error Handling
language: Go
comments_count: 4
repository_stars: 80174
---

When integrating with external AI/HTTP APIs, treat both transport errors and payload validity as first-class failures. Validate inputs, verify provider/HTTP status, and enforce response invariants—never silently accept partial or malformed data.

Apply these rules:
- Preconditions: return clear errors when required config is missing (API key/model) and decide explicitly for empty inputs (e.g., return empty embeddings/rerank scores).
- Status checks:
  - Check HTTP status (e.g., resp.StatusCode == http.StatusOK).
  - Also check provider-level status fields (e.g., BaseResp/status_code) before using returned data.
- Payload invariants:
  - Embeddings: for each returned item, validate index bounds and embedding presence; error if indices are out of range or embeddings are empty.
  - Rerank: validate every result index is within [0, len(texts)); error on out-of-range indices.
  - Count matching: if the API is expected to return one score per input (especially when you set top_n), error when result count doesn’t match.
- Defensive JSON decoding: when numeric fields may deserialize as different float types, guard and convert safely; add targeted tests for the guarded edge cases.

Example pattern (fail fast + invariant checks):

```go
resp, err := client.Do(req)
if err != nil { return nil, fmt.Errorf("send request: %w", err) }
defer resp.Body.Close()
body, err := io.ReadAll(resp.Body)
if err != nil { return nil, fmt.Errorf("read response: %w", err) }

if resp.StatusCode != http.StatusOK {
  return nil, fmt.Errorf("API error: %s body=%s", resp.Status, string(body))
}

// provider-level status (if present)
// var base BaseResp; json.Unmarshal(body,&base); if base.StatusCode!=0 { return nil, ... }

// invariants
embeddings := make([][]float64, len(texts))
for _, item := range parsed.Data {
  if item.Index < 0 || item.Index >= len(texts) {
    return nil, fmt.Errorf("unexpected index %d for %d inputs", item.Index, len(texts))
  }
  if len(item.Embedding) == 0 {
    return nil, fmt.Errorf("empty embedding for index %d", item.Index)
  }
  // convert with type guards to float64
}
```

Goal: errors should be deterministic and informative, and incorrect provider payloads should never silently degrade results (e.g., via skipped indices or indistinguishable default zeros).