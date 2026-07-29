---
title: Enforce Security Boundaries Early
description: 'Apply security controls at the controlling layer and before triggering
  any side effects.


  - **Iframe/sandbox:** Treat `sandbox` on ancestor iframes as the effective policy
  for descendants. Ensure the default sandbox includes any permissions required by
  the hosted app (otherwise functionality may break or be silently over-restricted).'
repository: aaif-goose/goose
label: Security
language: TSX
comments_count: 2
repository_stars: 51876
---

Apply security controls at the controlling layer and before triggering any side effects.

- **Iframe/sandbox:** Treat `sandbox` on ancestor iframes as the effective policy for descendants. Ensure the default sandbox includes any permissions required by the hosted app (otherwise functionality may break or be silently over-restricted).
- **Allowlists/URLs:** For deep links or user-provided URIs, validate and apply allowlist decisions **before** calling discovery or any backend operation that could fetch manifests, probe endpoints, or initialize services. Re-check after resolution for defense in depth.

Example pattern:
```ts
// (1) Correct effective sandbox policy at the controlling layer
iframe.setAttribute(
  'sandbox',
  sandbox.permissions || 'allow-scripts allow-same-origin allow-forms'
);

// (2) Early allowlist enforcement before backend side effects
const uri = new URL(link).searchParams.get('uri');
if (!uri) throw new Error('mcp deep link is missing the uri parameter');

// allowlist check MUST happen BEFORE discoverExtension
if (!isAllowedMcpUri(uri)) {
  throw new Error('Blocked MCP URI by allowlist');
}

const { data, error } = await discoverExtension({ body: { uri } });
// (defense in depth) optionally re-check resolved endpoint/host here
```

Use this as a review checklist for any code that:
1) constructs sandboxed browsing contexts, or 2) accepts URIs/deep links and performs discovery/network calls.