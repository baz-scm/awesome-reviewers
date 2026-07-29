---
title: Sorted Selection Safety
description: 'When code decides “latest/first/anchor” behavior (events, schedule steps,
  URL/mention parsing), it must be deterministic by construction: sort inputs by the
  relevant timestamp/field before using positional selection (e.g., findLast), use
  dedup keys at the correct granularity to avoid permanent suppression, and make regex/parsers
  unambiguous with correct...'
repository: QwenLM/qwen-code
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 26407
---

When code decides “latest/first/anchor” behavior (events, schedule steps, URL/mention parsing), it must be deterministic by construction: sort inputs by the relevant timestamp/field before using positional selection (e.g., findLast), use dedup keys at the correct granularity to avoid permanent suppression, and make regex/parsers unambiguous with correct anchors/lookarounds for the target grammar.

Apply this standard:
1) Sort before positional selection
- Do not assume API pagination ordering matches your intended “latest” semantics.
- Example pattern:

```ts
// Before selecting the most recent matching event
const events = await listEvents(...);
// Sort explicitly by created_at (or the actual field you reason about)
events.sort((a, b) => (a.created_at || '').localeCompare(b.created_at || ''));

const event = events.findLast((candidate) => {
  // apply your temporal/logic predicates against candidate.created_at
  return candidate.created_at && candidate.created_at > lowerBound;
});
```

2) Dedup keys must match the true identity of the unit being deduped
- If you want to dedupe per-event, do not dedupe by per-thread/per-entity stable ids.
- Example:

```ts
const notifKey = `${notification.id}|${notification.updated_at}`;
if (isDispatched(dispatchedNotifications, notifKey)) continue;
```

3) Regex/parsers: align grammar assumptions on both parse and emit sides
- Anchor the parse to the exact end-of-string you intend (avoid accidental first-match).
- Ensure lookahead/exclusion character sets reflect the target platform’s valid identifier characters.
- Add tests that cover the “grammar boundary” (e.g., trailing base path segments, dotted usernames, etc.).

Why: Without these properties, seemingly small changes (different pagination alignment, an extra character allowed by a platform, or a dedup key that’s too coarse) turn into permanent missing triggers, duplicate dispatches, or wrong attribution.