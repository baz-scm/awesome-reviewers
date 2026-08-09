---
title: Stable API Contracts
description: 'When designing or evolving API surfaces (including XPC/wire formats
  and CLI-to-client contracts), treat the request/response shape as a long-lived contract:
  keep it semantically high-level, strongly typed, and backward/forward compatible.'
repository: apple/container
label: API
language: Swift
comments_count: 6
repository_stars: 48787
---

When designing or evolving API surfaces (including XPC/wire formats and CLI-to-client contracts), treat the request/response shape as a long-lived contract: keep it semantically high-level, strongly typed, and backward/forward compatible.

Apply these rules:
1) **Don’t leak internals or require guesswork**
   - If the server needs an identifier, add it to the contract (e.g., `volumeName`) rather than inferring it from filesystem paths.
2) **Prefer single-shot high-level operations over exposing low-level steps**
   - If you need freeze/thaw, expose one operation that guarantees minimal freeze duration and correct sequencing.
3) **Stabilize wire format explicitly**
   - If you change Codable types (e.g., `URL` → `FilePath`), preserve the persisted/XPC encoding by custom encode/decode, and schedule migrations/breaking changes intentionally.
4) **Use strong types at API boundaries**
   - Accept `URL`/typed paths in the API, convert to strings/absolute representations only at the edge.
5) **Future-proof via optional structured fields**
   - Add optional request parameters (e.g., `dynamicEnv`) so new behaviors (SSH forwarding, bootstrap-time overrides) don’t require breaking signature changes.

Example (high-level operation + extensible bootstrap):
```swift
// Runtime API: single call encapsulates freeze/clone/thaw.
public func snapshotDisk(imagePath: String, destinationPath: String) async throws

// Bootstrap API: optional bootstrap-time overrides.
public func bootstrap(
  id: String,
  stdio: [FileHandle?],
  dynamicEnv: [String: String] = [:],
  sshAuthSocketPath: String? = nil
) async throws
```

If you must make a breaking change (e.g., wire encoding), ensure you also provide compatibility decoding for older payloads and/or a planned migration step rather than silently changing byte formats.