---
title: Optional-Safe Null Handling
description: 'Adopt a consistent null/absence policy:


  1) Model absence explicitly

  - If a value may be missing (older on-disk configs, optional server fields, optional
  UI inputs), represent it with an optional type (e.g., `String?`) and make the corresponding
  `Codable` field tolerant of omission.'
repository: apple/container
label: Null Handling
language: Swift
comments_count: 11
repository_stars: 48787
---

Adopt a consistent null/absence policy:

1) Model absence explicitly
- If a value may be missing (older on-disk configs, optional server fields, optional UI inputs), represent it with an optional type (e.g., `String?`) and make the corresponding `Codable` field tolerant of omission.

2) Prefer early-exit unwraps
- Use `guard let` / `if let` instead of force unwraps.
- For optional-derived values in loops, use `guard ... else { continue }`.

3) Use safe collection/dictionary defaults
- When mutating via a dictionary key, avoid `dict[key]!`.
- Prefer `dict[key, default: []].append(...)` or `dict[key]?.append(...)`.

4) Keep Codable backward-compatible
- When adding new fields to persisted data, use optional properties (or `decodeIfPresent`) so older files don’t fail to decode.

5) Avoid unnecessary optional boilerplate and optional-of-collection
- Don’t write redundant `= nil` for optional stored properties.
- Prefer `[T]` over `[T]?` unless you truly need to distinguish “missing” from “empty”.

Example patterns:

```swift
// 1) Codable backward compatibility
struct KubeConfig: Codable {
    enum CodingKeys: String, CodingKey {
        case currentContext = "current-context"
    }
    var currentContext: String? = nil
}

// 2) Dictionary mutation
allocationsBySession[session, default: []].append((hostname: hostname, index: index))

// 3) Safe unwrap in control flow
guard let lastName = file.lastComponent?.string else { continue }

// 4) Avoid optional-of-collection
struct VolumeListResponse: Codable {
    var warnings: [String] = [] // not [String]?
}

// 5) Avoid force unwrap parsing external data
guard let manifest = index.manifests.first else {
    throw ContainerizationError(.internalError, message: "Malformed image index")
}
```

Apply this standard anywhere you:
- mutate through optional subscripts,
- decode persisted/external data,
- derive strings/URLs/path components,
- convert from optional substrings.
