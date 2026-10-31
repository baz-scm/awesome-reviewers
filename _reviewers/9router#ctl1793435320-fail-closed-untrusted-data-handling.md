---
title: Fail-closed untrusted-data handling
description: 'Default every security-sensitive path to the most restrictive behavior,
  and never let untrusted or unconfigured input silently widen scope or leak data.
  Concretely:'
repository: decolua/9router#ctl1793435320
label: Security
language: JavaScript
comments_count: 5
repository_stars: 31733
---

Default every security-sensitive path to the most restrictive behavior, and never let untrusted or unconfigured input silently widen scope or leak data. Concretely:

- **Never leak secrets in responses.** Strip sensitive credential fields (e.g. `sessionToken`, API keys) from any serialized API response, even if they must remain available server-side for internal use. Build a single response-mapping helper (e.g. `toProviderConnectionResponse()`) and route all create/list/detail/update endpoints through it so redaction can't be forgotten on one path.
- **Sanitize before reflecting external content.** Any text taken from an upstream/third-party response (HTML error pages, provider error bodies, etc.) that gets surfaced to a client must be stripped of markup and length-clamped before being embedded in error messages or UI, to prevent XSS via untrusted content.
- **Honor explicit scope/authorization flags.** If a caller declares a restriction (e.g. `external_web_access:false`), never silently route around it (e.g. by falling back to an external provider) to "make it work." When the declared scope can't be honored, disable the feature entirely rather than relaxing the boundary.
- **Guard against identifier collisions.** When introducing internally reserved names/IDs that trigger privileged behavior (e.g. a fallback tool name executed automatically), check for collisions with user-supplied names first and bail out of the special-casing if one exists — otherwise attacker/user-controlled input can be executed as if it were trusted.
- **Fail closed on missing configuration.** Security- or privacy-relevant features (credential selection, data routing to a third party, etc.) must do nothing and return an explicit "not configured" error when unconfigured, rather than auto-selecting a provider/credential/account the user never opted into.

Example pattern for safe reflection of untrusted text:
```js
const bodyText = await upstreamResponse.text().catch(() => '');
const safeMessage = bodyText
  .replace(/<[^>]*>/g, '')      // strip markup
  .slice(0, 200);               // clamp length
streamController.handleError(safeMessage, upstreamResponse.status);
```
Apply this mindset during review: ask "what happens if this input is attacker-controlled or simply absent?" and require the safe/closed outcome by default.</description>
</invoke>
