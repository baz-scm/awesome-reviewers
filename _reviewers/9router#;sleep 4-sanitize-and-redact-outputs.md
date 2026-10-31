---
title: Sanitize and redact outputs
description: 'When building responses that combine server-side secrets, upstream data,
  or user-requested security scopes, always protect against leaking sensitive data
  and against reflecting untrusted content unsanitized. Specifically: (1) Never return
  sensitive credentials (API keys, session tokens, secrets) in client-facing API responses
  even if they must be retained...'
repository: decolua/9router#;sleep 4
label: Security
language: JavaScript
comments_count: 3
repository_stars: 31756
---

When building responses that combine server-side secrets, upstream data, or user-requested security scopes, always protect against leaking sensitive data and against reflecting untrusted content unsanitized. Specifically: (1) Never return sensitive credentials (API keys, session tokens, secrets) in client-facing API responses even if they must be retained server-side for signing or other internal use — strip them at the response-serialization boundary (e.g., `toProviderConnectionResponse()` should omit `sessionToken` from create/list/detail/update payloads). (2) Treat any content originating from an external/upstream source (error pages, HTML bodies, provider responses) as untrusted before it is surfaced to the end user — strip HTML tags, clamp length, and avoid directly embedding raw upstream text into error messages to prevent XSS. (3) Honor explicit security/privacy flags set by the caller (e.g., `external_web_access: false`) rather than silently overriding them with a fallback or default behavior that could expand scope or violate the user's intended restriction. In short: redact secrets before they leave the server, sanitize external input before it reaches the client, and never bypass an explicit security constraint for convenience.

Example:
```js
// Bad: raw upstream text reflected directly
const shortMsg = bodyText; // could contain <script> or secrets

// Good: sanitize before surfacing
const safeMsg = stripHtml(bodyText).slice(0, 200);
streamController.handleError(safeMsg, status);

// Bad: returning the secret because it was needed internally
return { profile, region, accessKeyId, sessionToken };

// Good: strip secrets at the API boundary
return { profile, region, accessKeyId }; // sessionToken kept server-side only
```