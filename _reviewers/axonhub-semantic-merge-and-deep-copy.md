---
title: Semantic Merge And Deep Copy
description: When your code incrementally merges or inherits structured data (JSON
  payloads, rule trees, settings), correctness should be enforced by (a) semantic,
  lossless reconciliation and (b) deep-copying every nested mutable component.
repository: looplj/axonhub
label: Algorithms
language: Go
comments_count: 2
repository_stars: 4808
---

When your code incrementally merges or inherits structured data (JSON payloads, rule trees, settings), correctness should be enforced by (a) semantic, lossless reconciliation and (b) deep-copying every nested mutable component.

Apply this standard:
1) For delta/stream/state reconciliation
- Treat the terminal value as canonical; allow equivalent representations (e.g., JSON key order/whitespace) but reject truly different semantics.
- Compute and forward only the missing suffix/delta to avoid overwriting accumulated content.
- Use lossless parsing for equality (e.g., preserve numeric precision with `json.Decoder.UseNumber()`), so equality checks don’t collapse distinct values.
- Fail explicitly on divergence to prevent emitting corrupted concatenated state.

Example (Go sketch):
```go
func reconcileDoneArguments(forwarded, done string) (string, error) {
  // If done is empty, never overwrite accumulated deltas.
  if done == "" { return "", nil }

  // Prefer semantic equivalence over string equality.
  eq, err := semanticJSONEqual(forwarded, done)
  if err != nil { return "", err }
  if eq { return "", nil } // nothing missing

  // Otherwise, forward only missing suffix when done starts with forwarded.
  if forwarded != "" && strings.HasPrefix(done, forwarded) {
    return strings.TrimPrefix(done, forwarded), nil
  }

  return "", fmt.Errorf("divergent arguments")
}

func semanticJSONEqual(a, b string) (bool, error) {
  var va, vb any
  da := json.NewDecoder(strings.NewReader(a)); da.UseNumber()
  db := json.NewDecoder(strings.NewReader(b)); db.UseNumber()
  if err := da.Decode(&va); err != nil { return false, err }
  if err := db.Decode(&vb); err != nil { return false, err }
  return reflect.DeepEqual(va, vb), nil
}
```

2) For inheritance/transformations via cloning
- Any “rule” object you copy should be treated as a tree: deep-copy the entire nested structure (e.g., `When` conditions and any nested condition nodes), not only the top-level struct.
- Ensure nested slices/maps are copied (create new backing arrays/maps) before mutation.
- Avoid pointer aliasing between original and inherited objects; aliasing will cause future changes in one to silently affect the other.

Checklist before merging PRs:
- Merge/reconcile: Are you comparing semantics with lossless parsing? Are you computing deltas/suffixes instead of overwriting? Do you explicitly error on divergence?
- Clone/inherit: Are all nested nodes and collections deep-copied so inherited mutations can’t affect originals?