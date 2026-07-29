---
title: Scoped API Contract
description: When implementing API-facing features, ensure request/response contracts
  are consistent across all code paths, correctly shaped for the upstream/downstream
  API, and complete under pagination/time-windowing.
repository: QwenLM/qwen-code
label: API
language: TypeScript
comments_count: 7
repository_stars: 26407
---

When implementing API-facing features, ensure request/response contracts are consistent across all code paths, correctly shaped for the upstream/downstream API, and complete under pagination/time-windowing.

Rules:
1) Keep serialization/parsing round-trips structurally identical
- If you build URLs/identifiers, the parser must mirror the writer (anchoring, last-vs-first match, greedy behavior). Add a round-trip test.

2) Validate upstream API method signatures and data fields
- Use real API response fields (no hand-written interfaces + unsafe casts to “make it compile”).
- Never call SDK methods with wrong positional argument shapes; prefer strongly typed wrappers and remove `as unknown as ...` casts.

3) Make state transitions scope-safe; don’t mix per-item windows with global cursor side effects
- If you update “read” state via a global API call, do not use per-notification timestamps from that response as a filter lower bound for other routes. Base time filtering on your own cursor window.
- If a fast-path attach changes semantics, reject contradictory caller input (e.g., requested identifiers) rather than silently ignoring it.

4) Ensure pagination/windowing is complete (no permanent omission)
- Avoid hard caps like `maxPages: 1`/small page limits when correctness requires fetching all items in the time window.
- For CLI/API aggregations (e.g., `gh api --paginate`), handle multi-page/NDJSON responses by flattening correctly and testing multi-page cases.

Example patterns:
- Round-trip URL parsing should be anchored and match writer behavior:
```ts
export function buildSessionPathname(currentPathname: string, sessionId?: string) {
  // ...builds /<base>/session/<id> consistently...
}

export function parseSessionId(pathname: string) {
  // Mirror writer: anchor to the last occurrence if writer used last-match logic.
  return pathname.match(/\/session\/([^/]+)\/?$/)?.[1];
}

// Test: expect(parseSessionId(buildSessionPathname('/app/session/', 'real-id'))) === 'real-id'
```
- Avoid wrong-typed external calls by removing casts and using correct method signatures:
```ts
// Prefer typed signatures; do not do api.Issues.show(chatId, { issueIId: ... })
// If SDK says show(issueId, { projectId }), pass issueId as number and projectId as string.
```
- For notification triggers, filter using your cursor window (not global last_read_at):
```ts
const windowSince = this.cursor.lastProcessedAt; // authoritative
// ...when scanning trigger events, treat created_at <= windowSince as lower-bound
```

Adopting these rules prevents silent drops, permanent omissions, and contract drift—common failure modes in API integration code.