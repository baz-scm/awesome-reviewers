---
title: Enforce trust boundaries
description: 'Treat every point where data crosses a trust boundary as a security
  checkpoint, not an afterthought. Concretely:


  1. Never leak secrets outward. Any response-shaping helper (e.g. `toProviderConnectionResponse()`)
  must strip credential fields such as `sessionToken`/`accessKeyId` from create, list,
  detail, and update responses even though the raw value is...'
repository: Decolua/9Router
label: Security
language: JavaScript
comments_count: 6
repository_stars: 31414
---

Treat every point where data crosses a trust boundary as a security checkpoint, not an afterthought. Concretely:

1. Never leak secrets outward. Any response-shaping helper (e.g. `toProviderConnectionResponse()`) must strip credential fields such as `sessionToken`/`accessKeyId` from create, list, detail, and update responses even though the raw value is still needed server-side for signing. Add a regression test that asserts the secret is absent from every response shape, not just the one you touched.

2. Never trust upstream/external content verbatim. If you reflect upstream error bodies, titles, or other untrusted text into a client-facing message, strip HTML/markup and clamp the length first — forwarding raw upstream HTML (e.g. a Cloudflare error page) into an error message is an XSS vector.

3. Default security/privacy-sensitive behavior to "off" or "deny" until explicitly configured, and make that default airtight end-to-end. For example, an unset `webSearchFallbackProvider` must not silently auto-pick the first credentialed provider — it should return a declined-search result pointing the user at settings, so no query is ever routed through a provider the user never chose.

4. Honor explicit scope/consent flags passed by the caller instead of overriding them for convenience — e.g. a request marked `external_web_access:false` must never be rerouted through an external provider; disable the feature entirely for that request instead.

5. Guard reserved internal identifiers (tool names, keys, routes) against collision with user- or client-supplied names. Before injecting an internal tool/field under a reserved name, check whether the caller already defined something with that name and bail out (return the input unchanged) rather than risk executing the caller's object as if it were your internal one.

```js
// Example: stripping a secret before it leaves the server, and sanitizing untrusted text
function toProviderConnectionResponse(connection) {
  const { providerSpecificData, ...rest } = connection;
  const { sessionToken, ...safeProviderData } = providerSpecificData || {};
  return { ...rest, providerSpecificData: safeProviderData }; // sessionToken never leaves the server
}

function safeUpstreamMessage(bodyText) {
  const stripped = bodyText.replace(/<[^>]*>/g, "").trim();
  return stripped.slice(0, 200); // never reflect raw/unbounded upstream HTML to the client
}
```

Apply this checklist (secret exposure, untrusted-content sanitization, secure-by-default behavior, scope honoring, and reserved-name collisions) whenever code crosses a client/server, upstream/downstream, or user-config/internal boundary.