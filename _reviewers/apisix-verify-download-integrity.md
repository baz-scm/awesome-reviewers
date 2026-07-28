---
title: Verify Download Integrity
description: When your code/CI downloads third-party binaries or packages and then
  installs them, verify integrity before installation (preferably SHA256/SHA256+signature).
  Store the expected checksum in versioned configuration keyed by the artifact/runtime
  version, and update it whenever you bump that version. Fail closed on mismatch.
repository: apache/apisix
label: Security
language: Shell
comments_count: 1
repository_stars: 16922
---

When your code/CI downloads third-party binaries or packages and then installs them, verify integrity before installation (preferably SHA256/SHA256+signature). Store the expected checksum in versioned configuration keyed by the artifact/runtime version, and update it whenever you bump that version. Fail closed on mismatch.

Example (pattern):

```sh
# expected SHA256 for this APISIX_RUNTIME lives in versioned config (.requirements)
APISIX_RUNTIME="${APISIX_RUNTIME}"
EXPECTED_SHA256="$(lookup_expected_sha256_for_runtime "$APISIX_RUNTIME")"
RELEASE_URL=".../${APISIX_RUNTIME}..."
DEB_NAME="..."
TMP_PATH="/tmp/$DEB_NAME"

wget --no-verbose --tries=3 --retry-connrefused "$RELEASE_URL" -O "$TMP_PATH"
ACTUAL_SHA256="$(sha256sum "$TMP_PATH" | awk '{print $1}')"

if [ "$ACTUAL_SHA256" != "$EXPECTED_SHA256" ]; then
  echo "Checksum mismatch for $DEB_NAME" >&2
  exit 1
fi

sudo apt-get install -y "$TMP_PATH"
rm -f "$TMP_PATH"
```

This prevents supply-chain/tampering attacks from being converted into installed code, and ensures upgrades remain secure by forcing explicit hash updates during runtime bumps.