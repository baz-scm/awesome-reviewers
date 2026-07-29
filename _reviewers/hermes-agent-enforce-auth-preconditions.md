---
title: Enforce auth preconditions
description: Security-sensitive state (e.g., creating/persisting a profile that assumes
  a working remote connection) must not be created when required authentication material
  is missing or invalid. If downstream token-auth/config saving will reject empty/placeholder
  tokens, block the flow up front or use a staged/OAuth flow so the local profile
  is only finalized after...
repository: nousresearch/hermes-agent
label: Security
language: TSX
comments_count: 1
repository_stars: 221948
---

Security-sensitive state (e.g., creating/persisting a profile that assumes a working remote connection) must not be created when required authentication material is missing or invalid. If downstream token-auth/config saving will reject empty/placeholder tokens, block the flow up front or use a staged/OAuth flow so the local profile is only finalized after auth/config persistence succeeds. If you can’t guarantee that, roll back local changes when remote auth/config saving fails.

Example pattern (block or stage before creating):

```ts
async function createRemoteProfile(params: {
  backendMode: 'remote' | 'local';
  token?: string;
  /* ... */
}) {
  if (params.backendMode === 'remote') {
    const token = params.token?.trim();
    if (!token) {
      throw new Error('Token required for remote connection');
      // OR initiate OAuth/staged setup here and return.
    }

    // Only after token is present, persist remote config.
    await window.hermesDesktop?.saveConnectionConfig?.({
      mode: 'remote',
      token,
    });
  }

  // Create/finalize local profile only after remote config succeeds.
  await createProfileAndPersist();
}
```