---
title: Require Download Digests
description: When downloading remote security-sensitive artifacts (e.g., kernels,
  binaries, containers), require an expected cryptographic digest (e.g., `sha256:<hex>`)
  and verify it before use. Treat missing digests for custom/variable URLs as a policy
  violation (fail closed) to prevent unverified or tampered downloads.
repository: apple/container
label: Security
language: Markdown
comments_count: 1
repository_stars: 48787
---

When downloading remote security-sensitive artifacts (e.g., kernels, binaries, containers), require an expected cryptographic digest (e.g., `sha256:<hex>`) and verify it before use. Treat missing digests for custom/variable URLs as a policy violation (fail closed) to prevent unverified or tampered downloads.

Example config pattern:
```toml
[kernel]
url = "https://example.com/artifact.tar.zst"
digest = "sha256:0123...abcd" # REQUIRED when url is custom/remote
```

Example enforcement pattern (pseudo-code):
```swift
let url: URL = config.url
let expectedDigest: String? = config.digest

guard let expectedDigest else {
  // Fail closed for non-default/custom URLs
  throw SecurityError.missingDigestForRemoteDownload
}

let data = try download(url)
let actualDigest = sha256(data)
precondition(actualDigest == expectedDigest)
```

Apply this to any code path that fetches from the network using a configurable URL and then executes/consumes the artifact.