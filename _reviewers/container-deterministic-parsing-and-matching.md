---
title: Deterministic Parsing And Matching
description: When implementing parsing and lookup/diff algorithms on strings/filesystems,
  guarantee determinism and correctness by (1) normalizing inputs into a canonical
  form before comparison/keying, (2) explicitly handling ambiguity instead of silently
  choosing an arbitrary match, and (3) deduping by semantic change keys while keeping
  a stable order.
repository: apple/container
label: Algorithms
language: Swift
comments_count: 7
repository_stars: 48787
---

When implementing parsing and lookup/diff algorithms on strings/filesystems, guarantee determinism and correctness by (1) normalizing inputs into a canonical form before comparison/keying, (2) explicitly handling ambiguity instead of silently choosing an arbitrary match, and (3) deduping by semantic change keys while keeping a stable order.

Apply this as standards:
- Normalize string tokens before parsing/using as keys (e.g., make unit/unit-suffix parsing case-insensitive; trim/strip format suffixes like CIDR masks: "ip/mask" → "ip").
- For “prefix” or fuzzy matching, treat multiple matches as an error (unless there is an exact match).
- For filesystem diffs where different traversal paths can produce duplicate semantic entries (hardlinks/bind mounts/symlinks), dedupe by a semantic key (e.g., (operation,path)) and then sort deterministically.
- Ensure string indexing/replacement is Unicode-safe (avoid mixing String.count/grapheme semantics with UTF-16 Range lengths).
- Use correct unit-multiplier semantics for storage sizes (kb/mb/gb = 10^3; KiB/MiB/GiB = 2^10).

Code sketch (ambiguous prefix matching):

```swift
func resolveSingleContainerID(prefix: String, candidates: [String]) throws -> String {
    let exact = candidates.first(where: { $0 == prefix })
    if let exact { return exact }

    let matches = candidates.filter { $0.hasPrefix(prefix) }
    guard matches.count <= 1 else {
        throw NSError(domain: "AmbiguousPrefix", code: 1,
                      userInfo: [NSLocalizedDescriptionKey: "Ambiguous prefix '
                          + prefix + "' matches: \(matches)"])
    }
    guard let only = matches.first else {
        throw NSError(domain: "NotFound", code: 2,
                      userInfo: [NSLocalizedDescriptionKey: "No match for prefix '"])
    }
    return only
}
```

Code sketch (stable dedupe by semantic key):

```swift
struct ChangeKey: Hashable { let op: Character; let path: String }

func dedupeStable<T>(items: [T], key: (T) -> ChangeKey) -> [T] {
    var seen = Set<ChangeKey>()
    var out: [T] = []
    out.reserveCapacity(items.count)
    for item in items {
        if seen.insert(key(item)).inserted { out.append(item) }
    }
    return out
}
```