---
title: Validate untrusted inputs
description: Treat CLI args, config, and IPC payloads as untrusted. Enforce semantic
  invariants at the boundary, then again during decoding/parsing (defense in depth),
  and add targeted negative tests.
repository: apple/container
label: Security
language: Swift
comments_count: 6
repository_stars: 48787
---

Treat CLI args, config, and IPC payloads as untrusted. Enforce semantic invariants at the boundary, then again during decoding/parsing (defense in depth), and add targeted negative tests.

Apply this especially to:
- Filesystem paths: normalize and reject invalid inputs (e.g., require absolute paths; don’t accept empty destinations). Validate both in `init()` and in `init(from:)`/private decode helpers.
- Numeric inputs: validate ranges and prevent signed→unsigned wraparound (e.g., negative timeouts).
- Structural/format inputs: reject wrong types (e.g., IPC messages not being dictionaries) and invalid ranges (e.g., ports).

Example pattern for path validation (init + decode):
```swift
struct PublishSocket: Codable {
  let containerPath: FilePath
  let hostPath: FilePath

  init(containerPath: FilePath, hostPath: FilePath) throws {
    guard containerPath.isAbsolute else {
      throw ContainerizationError(.invalidArgument, message: "containerPath must be absolute")
    }
    guard hostPath.isAbsolute else {
      throw ContainerizationError(.invalidArgument, message: "hostPath must be absolute")
    }
    self.containerPath = containerPath
    self.hostPath = hostPath
  }

  init(from decoder: Decoder) throws {
    let c = try decoder.singleValueContainer()
    // Decode as strings/plain wire form, then validate absoluteness here too.
    // If invalid: throw DecodingError.dataCorrupted(...)
  }
}
```

Checklist for new code:
1) Where is the input coming from (user/config/IPC)?
2) What invariant must always hold (absolute path, non-empty, existing dir vs file, allowed numeric range)?
3) Is validation performed before any unsafe conversion/usage?
4) If the value can come from persisted config, is it validated during `decode`/parsing too?
5) Do we have tests for invalid cases that previously could slip through (non-absolute path, negative timeout wraparound, port 0, wrong IPC type, digest mismatch/algorithm edge cases)?