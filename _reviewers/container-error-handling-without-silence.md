---
title: Error handling without silence
description: 'Treat errors as first-class: don’t blanket-suppress them with `try?`,
  `try!`, `_ =` result discards, or `2>/dev/null` unless you can prove the failure
  is expected and harmless. For unexpected failures, either propagate (`throw`) or
  explicitly log and recover in a deterministic way.'
repository: apple/container
label: Error Handling
language: Swift
comments_count: 13
repository_stars: 48787
---

Treat errors as first-class: don’t blanket-suppress them with `try?`, `try!`, `_ =` result discards, or `2>/dev/null` unless you can prove the failure is expected and harmless. For unexpected failures, either propagate (`throw`) or explicitly log and recover in a deterministic way.

Apply this rule:
- **Narrow suppression only**: when falling back for backward-compatibility, suppress only specific, expected cases (e.g. `keyNotFound`), and **throw** for malformed payloads.
- **Check system/OS calls**: capture return codes (and log warnings if you intentionally continue). Never ignore calls that can fail silently (e.g. `setsockopt`, iptables/systemctl).
- **Preserve failure signals in tests/cleanup**: don’t use `try?` where failures would corrupt subsequent state; either throw or record the failure.
- **Validate preconditions early**: ensure required inputs exist (e.g. “exactly one DNS question”, container running) and return an appropriate error/response variant.
- **Avoid crashing on bad inputs**: replace `fatalError` with typed thrown errors.

Example (narrow fallback instead of swallowing decode errors):
```swift
do {
  ipv4Address = try container.decode(CIDRv4.self, forKey: .ipv4Address)
} catch let DecodingError.keyNotFound(key, _) where key.stringValue == CodingKeys.address.stringValue {
  ipv4Address = try container.decode(CIDRv4.self, forKey: .address) // expected legacy fallback
}
// any other decoding error should be rethrown
```

Example (check OS call result / log warnings):
```swift
var sendSize = Self.socketSendBufferSize
let rc = setsockopt(fd, SOL_SOCKET, SO_SNDBUF, &sendSize, socklen_t(MemoryLayout<Int32>.size))
if rc != 0 {
  log.warning("setsockopt(SO_SNDBUF) failed with errno \(errno)")
  // either throw or continue deliberately after logging
}
```

This standard reduces silent misconfiguration, hidden data corruption, and hard-to-debug runtime/test failures while still allowing intentional, documented recovery paths.