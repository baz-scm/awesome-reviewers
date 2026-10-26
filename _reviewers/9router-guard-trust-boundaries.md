---
title: Guard trust boundaries
description: Treat every point where data crosses a trust boundary — server to client,
  client to server, or internal module to external provider — as a security checkpoint,
  not a pass-through.
repository: decolua/9router
label: Security
language: JavaScript
comments_count: 5
repository_stars: 31412
---

Treat every point where data crosses a trust boundary — server to client, client to server, or internal module to external provider — as a security checkpoint, not a pass-through.

- Never leak secrets in outbound responses. Credentials needed server-side (e.g. AWS `sessionToken`, API keys) must be stripped before serializing create/list/detail/update responses, even though the raw value stays available internally for signing requests. Centralize this in a single serializer so every endpoint benefits:
  ```js
  function toProviderConnectionResponse(connection) {
    const { sessionToken, ...safe } = connection.providerSpecificData ?? {};
    return { ...connection, providerSpecificData: safe };
  }
  ```
- Never reflect untrusted upstream/user content verbatim into responses or UI. Strip HTML/script content and clamp length before surfacing error bodies, titles, or other external text, to avoid XSS.
- Honor explicit security/privacy constraints set by the caller (e.g. `external_web_access: false`) rather than silently rerouting the request through a broader-scoped path; when such a flag is present, bypass the feature entirely instead of weakening the guarantee.
- When building internal/trusted identifiers that will later be treated as privileged (reserved tool names, internal flags, special routes), check for collisions with client-supplied data first and bail out of the rewrite if the name is already taken — otherwise untrusted input can impersonate a trusted mechanism and get executed with elevated trust.

Add a regression test for each boundary-crossing fix (e.g. asserting a secret is absent from every response, or that reserved names can't be hijacked) so these protections can't silently regress.</description>
</invoke>
