---
title: Env-aware gating and links
description: 'When code depends on environment configuration (feature flags, app base
  URLs, client attribution) or account identity, ensure you:


  1) **Gate UI/commands up front** using known state (feature flags + cheap session/workspace
  data + exposed connection state) so users don’t discover limitations only after
  running actions. Still perform **authoritative runtime...'
repository: cline/cline#v17
label: Configurations
language: TSX
comments_count: 4
repository_stars: 70883
---

When code depends on environment configuration (feature flags, app base URLs, client attribution) or account identity, ensure you:

1) **Gate UI/commands up front** using known state (feature flags + cheap session/workspace data + exposed connection state) so users don’t discover limitations only after running actions. Still perform **authoritative runtime checks** (e.g., dirty state, `ls-remote`) before executing.

2) **Centralize environment-specific URL building** (resolved base URL + attribution/client metadata). Avoid mixing configured URLs with hardcoded production URLs from the same screen.

3) **Separate environment config from account identity**: don’t add account-derived fields (e.g., privacy link inputs, user plumbing) to global context solely to support duplicate UI entries. Build account-related links in the component that already has the needed identity/config.

Example pattern (single URL builder + fallback + pre-gated UI):
```ts
function buildAppUrl(path: string, baseUrl?: string, attribution?: string) {
  const resolvedBase = baseUrl ?? "https://app.cline.bot"; // fallback to default
  const url = new URL(path, resolvedBase);
  if (attribution) url.searchParams.set("attribution", attribution);
  return url.toString();
}

// UI gating (cheap/known state)
const canShowCommand = featureFlagEnabled && (githubConnected ?? false);

// Runtime validation (authoritative)
async function runCommand() {
  await assertRepoClean();
  await assertRemoteAccessible();
  // ...execute
}
```
Adhering to this keeps behavior consistent across environments, prevents accidental prod/staging mismatches, and reduces brittle duplication created by configuration vs identity coupling.