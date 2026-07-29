---
title: Preserve signing entitlements
description: 'On macOS, treat re-signing (including ad-hoc re-sign after quarantine
  stripping) as a security-sensitive operation: preserve the app’s entitlements for
  the main bundle and any helper apps. Otherwise, macOS TCC access (mic/screen audio)
  may break or continuously prompt because the re-signed artifacts no longer carry
  the expected entitlements. Also ensure...'
repository: nousresearch/hermes-agent
label: Security
language: Shell
comments_count: 1
repository_stars: 221948
---

On macOS, treat re-signing (including ad-hoc re-sign after quarantine stripping) as a security-sensitive operation: preserve the app’s entitlements for the main bundle and any helper apps. Otherwise, macOS TCC access (mic/screen audio) may break or continuously prompt because the re-signed artifacts no longer carry the expected entitlements. Also ensure every packaging/update path uses the same entitlement-preserving logic.

Practical rule:
- If you strip quarantine and re-sign (e.g., `codesign --force --deep --sign -`), then re-apply the correct entitlements to both main and helper bundles.
- Centralize signing logic or ensure sibling scripts/paths call the same entitlement-preserving function.
- Skip the ad-hoc re-sign clobber behavior when a real signing identity is configured.

Example (bash pattern):
```bash
# Only for macOS ad-hoc path; skip when real signing is configured.
if [ "$OS" = "macos" ] && [ -z "${CSC_LINK:-}" ] && [ -z "${APPLE_SIGNING_IDENTITY:-}" ] && command -v codesign >/dev/null 2>&1; then
  xattr -cr "$app" 2>/dev/null || true

  main_entitlements="$desktop_dir/electron/entitlements.mac.plist"
  helper_entitlements="$desktop_dir/electron/entitlements.mac.inherit.plist"

  if [ -f "$main_entitlements" ] && [ -f "$helper_entitlements" ]; then
    # main bundle
    codesign --force --deep --sign - --entitlements "$main_entitlements" "$app" >/dev/null 2>&1 || true

    # helper apps inside the bundle
    while IFS= read -r -d '' helper_app; do
      codesign --force --deep --sign - --entitlements "$helper_entitlements" "$helper_app" >/dev/null 2>&1 || true
    done < <(find "$app" -type d -name "*.app" -print0)
  fi
fi
```
Apply this pattern consistently across all build/update routes so security-relevant signing behavior can’t drift.