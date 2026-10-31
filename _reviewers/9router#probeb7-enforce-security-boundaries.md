---
title: Enforce security boundaries
description: Treat every point where data crosses a trust boundary (API response,
  error message, tool injection) as a place to actively enforce security, not just
  assume safety by default.
repository: decolua/9router#probeB7
label: Security
language: JavaScript
comments_count: 5
repository_stars: 31737
---

Treat every point where data crosses a trust boundary (API response, error message, tool injection) as a place to actively enforce security, not just assume safety by default.

- Never return secrets/credentials in API output. Use an explicit allow-list serializer (e.g. `toProviderConnectionResponse()`) that strips sensitive fields like `sessionToken` or `accessKeyId` from every response path (create, list, detail, update), while keeping them available server-side only where strictly needed (e.g. for signing). Add regression tests asserting the secret is absent from each response shape.
- Never reflect untrusted external content (upstream error bodies, HTML titles, provider messages) into a client-facing message without sanitizing it first: strip HTML/script tags and clamp the length before it is shown or logged back to the user, to prevent stored/reflected XSS.
  ```js
  const shortMsg = stripHtml(titleMatch?.[1]?.trim() || bodyText).slice(0, 200);
  ```
- Honor security/privacy scope flags the caller explicitly set (e.g. `external_web_access: false`); never silently widen scope by rerouting a restricted request through a broader-access path. When such a flag is present, disable the rewrite entirely and forward the request unchanged.
- Guard reserved internal identifiers (tool names, keys, routes) against collision with client-supplied names. Before injecting or trusting an internal identifier, check whether the caller already defined one with the same name, and skip the injection/override if so — otherwise client input can hijack trusted internal behavior.

Any change that touches data serialization, error propagation, or tool/parameter injection should include a test proving the sensitive value is stripped, the untrusted content is sanitized, and declared scope/reserved-name constraints are respected.</description>
