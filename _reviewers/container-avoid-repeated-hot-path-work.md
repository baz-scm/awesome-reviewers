---
title: Avoid repeated hot-path work
description: In performance-sensitive code, avoid doing expensive operations repeatedly
  inside loops (repeated flattening/sorting, repeated filesystem attribute resolution,
  repeated regex/compiler/formatter construction, repeated list+search scans). Also
  ensure your tree/hierarchy logic uses consistent keys for both ordering and relationship
  detection.
repository: apple/container
label: Performance Optimization
language: Swift
comments_count: 7
repository_stars: 48787
---

In performance-sensitive code, avoid doing expensive operations repeatedly inside loops (repeated flattening/sorting, repeated filesystem attribute resolution, repeated regex/compiler/formatter construction, repeated list+search scans). Also ensure your tree/hierarchy logic uses consistent keys for both ordering and relationship detection.

Apply these practices:
- Hoist/cache heavy objects used per call (e.g., formatters, regex).
- Don’t re-build global intermediate structures inside inner loops (e.g., avoid flatMap+sort per node); restructure the algorithm to compute parent candidates once or maintain incremental state.
- Prefer bulk APIs over “list+search per item” patterns.
- Request needed filesystem attributes in bulk; resolve symlink targets only when necessary.
- Avoid allocation-heavy functional chains in hot paths; prefer lazy/nested loops that can stop early.
- Pre-size collections using the final workload size (after deduping/filtering).

Example (hoist cached regex):
```swift
extension GraphBuilder {
    private static let argSubRegex: NSRegularExpression = {
        try! NSRegularExpression(pattern: #"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"#)
    }()

    func substituteArgs(_ input: String, inFromContext: Bool) -> String {
        // use Self.argSubRegex here (don’t compile per call)
        // ...
        return input
    }
}
```

Example (avoid reserveCapacity mismatch):
```swift
let mounts = mounts.dedupe()
var result: [Filesystem] = []
result.reserveCapacity(mounts.count)
```

If a change introduces a new loop over many elements, re-check for inner-loop allocations, repeated sorting/flattening, repeated filesystem operations, and repeated scans/caches not being reused.