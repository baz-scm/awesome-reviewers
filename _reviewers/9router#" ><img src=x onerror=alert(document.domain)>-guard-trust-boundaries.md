---
title: Guard trust boundaries
description: Every point where data crosses a trust boundary (server→client, upstream→client,
  user config→system behavior, internal namespace→user input) must be explicitly validated
  or sanitized, never assumed safe.
repository: decolua/9router#" ><img src=x onerror=alert(document.domain)>
label: Security
language: JavaScript
comments_count: 5
repository_stars: 31680
---

Every point where data crosses a trust boundary (server→client, upstream→client, user config→system behavior, internal namespace→user input) must be explicitly validated or sanitized, never assumed safe.

Apply this in four ways:
1. **Never leak secrets outward.** Fields needed only for internal operations (e.g., an AWS `sessionToken` used for request signing) must be stripped from any response returned to the client, even though they're kept server-side for processing. Audit all API response builders for fields that should stay server-only.
2. **Sanitize untrusted external content before reflecting it.** If an upstream service returns raw HTML/text (e.g., an error page) that gets surfaced in a client-facing message, strip tags/markup and clamp length before including it, to avoid reflected XSS via untrusted upstream content.
3. **Never let automatic/fallback logic silently override explicit security or privacy configuration.** If a user has disabled a capability (e.g., `external_web_access:false`) or left a feature unconfigured, do not auto-select a substitute (like picking some other provider or rerouting to an external service). Treat "off" and "unconfigured" as hard stops, not defaults to be worked around.
4. **Protect reserved/internal identifiers from collision with user-supplied input.** Before trusting an internal name, tool, or key (e.g., a reserved fallback tool name) as privileged, check whether user-supplied data already claims that identifier — otherwise user input could be executed/trusted as if it were the internal mechanism.

Example (stripping a secret from a response):
```js
function toProviderConnectionResponse(conn) {
  const { sessionToken, ...safe } = conn.providerSpecificData; // never serialize sessionToken to the client
  return { ...conn, providerSpecificData: safe };
}
```

When adding new response shapes, fallback behaviors, or namespaced identifiers, explicitly consider: "What is on the other side of this boundary, and can it be trusted?" If not, add a sanitation, stripping, or collision check — and cover it with a regression test, as was done for each fix above.