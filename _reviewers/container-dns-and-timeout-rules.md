---
title: DNS and Timeout Rules
description: When implementing networking features (DNS, proxies, RPC/XPC), make behavior
  consistent with the correct layer and avoid imposing policy that breaks end-to-end
  semantics.
repository: apple/container
label: Networking
language: Swift
comments_count: 4
repository_stars: 48787
---

When implementing networking features (DNS, proxies, RPC/XPC), make behavior consistent with the correct layer and avoid imposing policy that breaks end-to-end semantics.

Guidelines:
1) Separate DNS defaults by layer
- Keep host/apiserver DNS defaults distinct from in-container `resolv.conf` defaults.

2) Normalize DNS names end-to-end
- Ensure parse/store/lookup all normalize the same way (e.g., treat `foo` and `foo.` consistently).
- Add focused unit tests for normalization.

3) Make forwarding timeouts cascade
- If one service forwards an XPC call to another, don’t add an arbitrary timeout in the outer layer when the inner layer is responsible for timing out. Otherwise, pick a timeout based on the specific operation.

4) Decode DNS safely
- Validate compression pointers and guard against malformed packets that could cause loops.

Example (timeout cascading):
```swift
// In the forwarding client: remove arbitrary timeout when the downstream call cascades timeouts.
let _ = try await xpcSend(message: request)
```
Example (DNS normalization idea):
```swift
func normalize(_ hostname: String) -> String {
    let s = hostname.hasSuffix(".") ? String(hostname.dropLast()) : hostname
    return s.lowercased()
}
```