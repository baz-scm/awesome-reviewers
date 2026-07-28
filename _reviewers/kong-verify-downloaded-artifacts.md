---
title: Verify Downloaded Artifacts
description: 'Any CI/install workflow that downloads a binary or other external artifact
  must verify its integrity before use.


  Apply this standard:

  - Prefer immutable references (commit SHA/immutable artifact IDs) when your tooling
  supports it.'
repository: Kong/kong
label: Security
language: Txt
comments_count: 1
repository_stars: 43871
---

Any CI/install workflow that downloads a binary or other external artifact must verify its integrity before use.

Apply this standard:
- Prefer immutable references (commit SHA/immutable artifact IDs) when your tooling supports it.
- Otherwise, download deterministically (e.g., by version/tag) and verify a pre-published cryptographic hash (sha256) at install time.
- Fail closed: if the computed hash doesn’t match the expected hash, abort the install.

Example pattern (shell):
```sh
EXPECTED_SHA256="46847521abf3745686d89460809b84e6a9f10e33"  # trusted/pre-published
URL="https://example.com/tool/releases/download/vX.Y.Z/tool-linux-x64"
curl -fsSL "$URL" -o tool
ACTUAL_SHA256=$(sha256sum tool | awk '{print $1}')
if [ "$ACTUAL_SHA256" != "$EXPECTED_SHA256" ]; then
  echo "sha256 mismatch: expected $EXPECTED_SHA256 got $ACTUAL_SHA256" >&2
  exit 1
fi
# proceed to use tool only after verification
```