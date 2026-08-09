---
title: Document invariants and changes
description: 'When introducing/altering API fields, parsing rules, or behavior, ensure
  documentation makes the code’s correctness contract explicit.


  Apply this standard:'
repository: apple/container
label: Documentation
language: Swift
comments_count: 5
repository_stars: 48787
---

When introducing/altering API fields, parsing rules, or behavior, ensure documentation makes the code’s correctness contract explicit.

Apply this standard:
- Document parameter semantics and any constraints/invariants in docc (what formats are allowed, required normalization, valid ranges).
- Enforce those constraints in the initializer/validation layer so values are valid “by construction.”
- For breaking type/behavior changes, add versioned doc comments (what changed, since when) and any temporary compatibility guarantees (e.g., decoder handling old representations).
- If behavior is intentionally non-obvious (e.g., ignoring timestamps for determinism), keep a short rationale comment next to the logic and/or visible flags so future changes don’t “fix” it back.
- Keep docs truthful: don’t mention defaults or normalization rules that aren’t actually implemented.

Example (initializer contracts + documented change):
```swift
/// Represents a socket to be published from container to host.
public struct PublishSocket: Sendable, Codable {
    /// Container-side socket path.
    /// Constraints: must be an absolute path within the container filesystem.
    public let containerPath: FilePath

    /// Host-side socket path.
    /// Constraints: must be an absolute path and must not be a directory.
    public let hostPath: FilePath

    /// Deprecated: New in 1.0.0; path types changed from `URL` to `FilePath`.
    /// Note: Decoder currently accepts both `URL` and `FilePath` for backward compatibility.
    public init(containerPath: FilePath, hostPath: FilePath) throws {
        // Enforce invariants here so instances are correct by construction.
        guard containerPath.isAbsolute else { throw ValidationError.invalidContainerPath }
        guard hostPath.isAbsolute else { throw ValidationError.invalidHostPath }
        self.containerPath = containerPath
        self.hostPath = hostPath
    }
}
```