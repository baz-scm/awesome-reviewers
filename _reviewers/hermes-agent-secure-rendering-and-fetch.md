---
title: Secure Rendering And Fetch
description: 'All untrusted inputs must be hardened at their security boundaries:
  (1) for network calls, validate the destination on every redirect hop (and ideally
  after DNS resolution), and (2) for any rendered or embedded output, sanitize/encode
  for the exact output context to prevent XSS and script-breaking.'
repository: nousresearch/hermes-agent
label: Security
language: Other
comments_count: 9
repository_stars: 221948
---

All untrusted inputs must be hardened at their security boundaries: (1) for network calls, validate the destination on every redirect hop (and ideally after DNS resolution), and (2) for any rendered or embedded output, sanitize/encode for the exact output context to prevent XSS and script-breaking.

Apply this standard:
- Network requests (SSRF prevention)
  - Do not rely on validating only the original URL/hostname when `redirect` is enabled.
  - Handle redirects manually: for each hop, validate protocol, host, and block private/loopback/link-local and reserved IP ranges (including IPv6). Prefer validating after resolving the hostname to an IP.
  - Enforce the same redirect policy for any derived URLs (e.g., image downloads).
- Rendering/output encoding (XSS prevention)
  - Do not “strip” HTML with regex unless you have a strict allowlist sanitizer.
  - Reject or sanitize all event handlers/unsafe attributes (quoted and unquoted forms) and dangerous tags/URLs.
  - When embedding JSON into an HTML `<script>` block, escape `</script>` (and other context-breaking sequences) before interpolation.
  - Add regression tests for representative payloads (redirect chains; `</script>` and unquoted `onerror` payloads).

Example pattern for safe redirects (sketch):
```js
async function fetchWithValidatedRedirects(initialUrl, validateHop) {
  let url = initialUrl;
  for (let hops = 0; hops < 5; hops++) {
    validateHop(url); // block private/loopback/reserved + enforce allowlist
    const res = await fetch(url, { redirect: 'manual' });
    if (res.status < 300 || res.status >= 400) return res;
    const loc = res.headers.get('location');
    if (!loc) return res;
    url = new URL(loc, url).href;
  }
  throw new Error('Too many redirects');
}
```

And for JSON-in-script embedding, ensure you escape for script context (e.g., replace `</script>` with `<\/script>` before injecting).