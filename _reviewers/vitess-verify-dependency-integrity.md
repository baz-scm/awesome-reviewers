---
title: Verify dependency integrity
description: Always verify the integrity of external dependencies, especially those
  downloaded from non-official or personal repositories. This helps prevent supply
  chain attacks where compromised packages could introduce security vulnerabilities.
repository: vitessio/vitess
label: Security
language: Yaml
comments_count: 1
repository_stars: 19815
---

Always verify the integrity of external dependencies, especially those downloaded from non-official or personal repositories. This helps prevent supply chain attacks where compromised packages could introduce security vulnerabilities.

When downloading external packages:
1. Prefer official sources over personal repositories
2. Always validate package integrity using cryptographic checksums (SHA-256 recommended)
3. Fail the build/installation if verification fails
4. Document the expected checksums in your codebase

Example implementation:
```bash
# Download package
wget -c https://example.com/package.deb

# Define expected checksum
EXPECTED_SHA256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

# Verify checksum and abort on mismatch
echo "$EXPECTED_SHA256 package.deb" | sha256sum -c - || { echo "Checksum verification failed!"; exit 1; }

# Only proceed with installation if verification passed
sudo dpkg -i package.deb
```

For long-term solutions, work towards hosting critical dependencies in organization-controlled repositories with proper access controls and provenance tracking.