---
title: Deterministic Cache Keys
description: 'Cache keys must be built only from inputs that truly change model output,
  and must be deterministic, complete, and cheap to compute.


  **Rules**

  1. **Derive keys from a stable message “anchor”.** If using conversation head hashing,
  explicitly define which roles and how many bytes you consider (e.g., contiguous
  leading `system`/`developer`, plus first...'
repository: looplj/axonhub
label: Caching
language: Go
comments_count: 3
repository_stars: 4808
---

Cache keys must be built only from inputs that truly change model output, and must be deterministic, complete, and cheap to compute.

**Rules**
1. **Derive keys from a stable message “anchor”.** If using conversation head hashing, explicitly define which roles and how many bytes you consider (e.g., contiguous leading `system`/`developer`, plus first `user`). Keep later turns from changing the head anchor when that’s intended.
2. **Include all message modalities in the fingerprint.** Don’t hash only `text`; include non-text parts (image/video/document/audio/etc.) using a consistent scheme. When hashing variable-sized units, include **length prefixes** (or other unambiguous framing) so different payloads that share a prefix don’t collide.
3. **Do not let unrelated metadata affect cache hits.** If you inject IDs (user/session/order IDs, fake IDs, routing metadata), ensure caching is driven solely by the message content (and any explicitly required rule/settings signatures).
4. **Keep cache-key work lightweight on hot paths.** Avoid full JSON serialization during cache lookup. For invalidation due to developer-rule/settings changes, add a **compact per-field signature** (e.g., FNV or similar) computed from only the fields that affect candidate/routing behavior.

**Sketch (Go-like pseudocode)**
```go
// Cache key inputs: (1) stable message anchor, (2) cheap settings/rules signature.
func cacheKey(messages []Message, rulesSig uint64, sessionID string) string {
    anchor := conversationAnchor(messages) // includes text + non-text parts with framing
    return fmt.Sprintf("%s|%d|%s", anchor, rulesSig, sessionID)
}

func conversationAnchor(messages []Message) string {
    // Hash only: leading system/developer + first user (bounded by anchorMaxBytes)
    // For each message: role + delimiter + all content parts.
    // For each part:
    //   - if text: write length prefix + text
    //   - if non-text: write part kind + length prefix + URL/data bytes
    // Ensure deterministic ordering and framing.
}
```

**Outcome**
- Correctness: different prompts (including non-text variations) don’t share the same cached response.
- Performance: key computation stays in the hot path without heavy serialization.
- Hit rate: unrelated metadata changes don’t bust caches unexpectedly.