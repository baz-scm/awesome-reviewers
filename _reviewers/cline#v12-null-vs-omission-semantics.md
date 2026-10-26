---
title: Null vs Omission Semantics
description: When a field’s meaning depends on whether it was **omitted**, **explicitly
  null**, or **explicitly empty**, treat those as distinct states and encode that
  distinction at boundaries.
repository: cline/cline#v12
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70872
---

When a field’s meaning depends on whether it was **omitted**, **explicitly null**, or **explicitly empty**, treat those as distinct states and encode that distinction at boundaries.

Practical rules:
1) **Omitted (`undefined`) ⇒ don’t send the field** (no change / keep stored value).
2) **Explicit reset (`null`) ⇒ send literal `null`** only if the receiving contract defines it as a reset.
3) **Empty (`[]`, `""`) ⇒ send it as an actual user value**; do not “nullish coalesce” away empty collections.
4) If external inputs can contain `null` where your domain expects “string or omitted”, **normalize at the boundary** (e.g., convert `null` to omission), and make the TS types match the normalization.

Example (request building):
```ts
type Updates = {
  prompt?: string | undefined; // omitted => no change
  metadata?: Record<string, unknown> | undefined;
  baseUrl?: string | null | undefined; // null => explicit reset (contract-dependent)
};

function toPayload(u: Updates) {
  return {
    ...(u.prompt !== undefined ? { prompt: u.prompt } : {}),
    ...(u.metadata !== undefined ? { metadata: u.metadata } : {}),
    // Only send literal null if the downstream contract treats it as a reset
    ...(u.baseUrl !== undefined ? { baseUrl: u.baseUrl } : {}),
  };
}
```

Example (preserve empty arrays on retry-like flows):
```ts
async function retryWithAttachments(retry: { images?: string[] }, imagesFromUI?: string[]) {
  const imagesToSend = imagesFromUI?.length ? imagesFromUI : retry.images;
  // ensures [] from UI doesn’t get treated like “missing”; only swaps when UI provides no attachments
  return imagesToSend;
}
```

Applying this consistently prevents “no-op resets”, wrong defaulting, and subtle behavior changes caused by treating `null`, `undefined`, and empty values as interchangeable.