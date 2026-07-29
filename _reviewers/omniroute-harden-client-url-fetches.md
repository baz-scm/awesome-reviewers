---
title: Harden Client URL Fetches
description: Any client-controlled URL (including OpenAI image_url) must be treated
  as SSRF-/DoS-/parsing-risk input and validated *at every transition* before connecting.
repository: diegosouzapw/OmniRoute
label: Security
language: TypeScript
comments_count: 8
repository_stars: 33162
---

Any client-controlled URL (including OpenAI image_url) must be treated as SSRF-/DoS-/parsing-risk input and validated *at every transition* before connecting.

Apply this standard:
- **Strict outbound policy:** allow only http(s); reject embedded creds, localhost, link-local/private/CGNAT, and metadata hostnames.
- **Redirect safety:** use `redirect: "manual"`; for each hop, resolve + validate again and enforce a small maximum redirect count.
- **DNS rebinding safety:** after hostname validation, resolve IPs and reject if *any* resolved address is private/local/link-local/metadata.
- **Resource caps:** cap wall-clock fetch time and final decoded/received size (and ideally cheap pre-checks).
- **Content integrity:** verify `content-type` (and for `data:` URLs: enforce `image/*`, base64-only as required).
- **Fail closed with sanitized errors:** throw a 400-class error with a message that does not echo attacker-controlled URLs/hosts.
- **No “wildcard” targets for client-driven messaging:** when sending `postMessage`, explicitly target the intended loopback origins (no `*`).

Example pattern (server-side fetch):
```ts
async function safeFetchImageBytes(inputUrl: string) {
  // 1) Parse + enforce strict outbound policy
  let current = inputUrl;
  for (let hop = 0; hop <= 3; hop++) {
    const parsed = parseAndValidatePublicUrl(current); // strict scheme/host policy

    // 2) DNS rebinding defense (reject if any IP answer is private)
    // validateResolvedIps(parsed.hostname)

    // 3) Manual redirect handling
    const res = await fetch(parsed.toString(), { method: 'GET', redirect: 'manual' });
    if (res.status >= 300 && res.status < 400 && res.headers.get('location')) {
      current = new URL(res.headers.get('location')!, parsed).toString();
      continue; // re-validate next hop
    }

    // 4) Verify content-type and read with a size cap
    const ct = (res.headers.get('content-type') || '').toLowerCase();
    if (!ct.startsWith('image/')) throw new Error('Image content-type required');
    const data = await readCapped(res, 1 * 1024 * 1024);
    return data;
  }
  throw new Error('Too many redirects');
}
```