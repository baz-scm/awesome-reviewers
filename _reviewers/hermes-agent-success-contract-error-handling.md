---
title: Success Contract Error Handling
description: 'Define a single “success contract” for each step: only report ok/success
  if the operation is actually accepted; for optional steps, convert failures into
  a structured soft-skip (but still record a diagnostic reason).'
repository: nousresearch/hermes-agent
label: Error Handling
language: Other
comments_count: 4
repository_stars: 221948
---

Define a single “success contract” for each step: only report ok/success if the operation is actually accepted; for optional steps, convert failures into a structured soft-skip (but still record a diagnostic reason).

Apply these rules:
1) Optional work ⇒ soft-skip with reason
- Wrap optional installs/steps in try/catch.
- On failure, set a skip reason channel/field and return without aborting the parent flow.

2) Required work ⇒ hard-fail
- For filesystem/network writes that are meant to change state, don’t swallow errors.
- If you truly want idempotency, handle the known safe case explicitly (e.g., EEXIST) and surface all other errors.

3) API writes ⇒ treat provider error channels as failures
- If GraphQL/REST returns explicit error collections (e.g., Shopify `userErrors`), treat non-empty as a failure even if the HTTP/transport succeeded.
- After a mutation, verify the returned resource/fields reflect the approved changes before reporting execute-mode success.

Example (optional step soft-skip)
```js
async function stageBrowser({ hasNode, skipReasonRef, SkipChromium }) {
  if (!hasNode) {
    skipReasonRef.value = 'Node.js unavailable; optional browser tooling skipped';
    return { skipped: true };
  }
  try {
    await InstallAgentBrowser({ SkipChromium });
    return { skipped: false };
  } catch (e) {
    skipReasonRef.value = `agent-browser install failed: ${String(e?.message || e)}`;
    // Do NOT rethrow: optional degradation
    return { skipped: true };
  }
}
```

Example (GraphQL mutation userErrors)
```js
async function applyMutationOrFail(client, mutation, variables) {
  const data = await gql(client, mutation, variables);
  const result = data?.[/* mutation root field */] || data;
  const userErrors = result?.userErrors || [];
  if (userErrors.length) {
    throw new Error(`Mutation rejected by API: ${JSON.stringify(userErrors)}`);
  }
  // Optionally verify returned fields match the approved inputs here.
  return result;
}
```

Outcome: fewer false “ok:true” results, predictable graceful degradation for optional features, and consistent diagnostics when failures happen.