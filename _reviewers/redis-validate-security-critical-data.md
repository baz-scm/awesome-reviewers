---
title: Validate security-critical data
description: When code consumes security-critical data—either to perform privileged
  state changes at runtime or to download/execute external artifacts—it must validate
  integrity/invariants before proceeding.
repository: redis/redis
label: Security
language: Other
comments_count: 2
repository_stars: 74261
---

When code consumes security-critical data—either to perform privileged state changes at runtime or to download/execute external artifacts—it must validate integrity/invariants before proceeding.

Apply these checks:
- Runtime guardrails for powerful flags: For any command that can force behavior (e.g., recovery/replay/creation), validate that referenced resources actually exist and that the operation will not create inconsistent/phantom state. If validation fails, skip or reject deterministically.
- Supply-chain artifact integrity: For build/dependency downloads, verify the downloaded file using the correct checksum from the official source for the exact artifact you download (e.g., don’t mix tar.gz vs tar.xz checksums).

Example (runtime invariant + safe skip):
```c
// Pseudocode for a FORCE-like path
if (force_enabled) {
    if (!stream_entry_exists(stream_id)) {
        // Prevent phantom state creation
        return OK_WITHOUT_MUTATION; // or skip this ID
    }
    create_pel_entry(...); // only after invariant holds
}
```

Example (build checksum verification):
```sh
RUST_VERSION=1.94.0
# Ensure checksum matches the exact downloaded artifact
RUST_SHA256='9a358120ce1491a4d5b7f71a41e4e97b380b5db5d4ec31f7110f5b3090bd3d55'
curl -sSLO "$URL"  # URL must point to the same tarball as the checksum
echo "$RUST_SHA256  $(basename "$URL")" | sha256sum -c -
```