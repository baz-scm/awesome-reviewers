---
title: Scope APT Signing Keys
description: When configuring APT repositories in install scripts, scope trust to
  a dedicated signing key and avoid deprecated/global keys. Don’t hardcode `amd64`;
  derive the architecture so the repo source is correct for non-amd64 systems.
repository: Azure/azure-cli
label: Security
language: Shell
comments_count: 1
repository_stars: 4592
---

When configuring APT repositories in install scripts, scope trust to a dedicated signing key and avoid deprecated/global keys. Don’t hardcode `amd64`; derive the architecture so the repo source is correct for non-amd64 systems.

Apply this checklist:
1) Use `signed-by=/path/to/keyring.gpg` in the `deb` line for the repository.
2) Remove deprecated keys from the general keyring if your script previously installed them, to prevent duplicate/ambiguous trust.
3) Avoid hardcoding `arch=amd64`; use `dpkg --print-architecture` so arm64 (and others) work correctly.

Example:
```sh
arch="$(dpkg --print-architecture)"
keyring_dir="/etc/apt/keyrings"
keyring_path="$keyring_dir/microsoft.gpg"

# (Optional) clean deprecated keys if present to avoid duplicate trust
# rm -f /etc/apt/trusted.gpg.d/microsoft*.gpg

echo "deb [arch=${arch} signed-by=${keyring_path}] https://packages.microsoft.com/repos/azure-cli ${CLI_REPO} main" \
  > /etc/apt/sources.list.d/microsoft-azure-cli.list
```