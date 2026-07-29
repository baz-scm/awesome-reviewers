---
title: Enforce Security End-to-End
description: When implementing security controls, treat them as end-to-end requirements
  across *all* navigation paths and *all* auth/transport interfaces. Two common failure
  modes are (1) hidden/aux renderer windows that still allow unintended credential/WebAuthn
  UI via a fallback path, and (2) security-sensitive flows that accept security context
  but some callers pass...
repository: nousresearch/hermes-agent
label: Security
language: TypeScript
comments_count: 2
repository_stars: 221948
---

When implementing security controls, treat them as end-to-end requirements across *all* navigation paths and *all* auth/transport interfaces. Two common failure modes are (1) hidden/aux renderer windows that still allow unintended credential/WebAuthn UI via a fallback path, and (2) security-sensitive flows that accept security context but some callers pass plain public URLs, causing bypass of the intended secure routing/transport.

Apply this standard:
- Remove or fully harden fallback paths: if a component can admit arbitrary/public pages into a hidden renderer, ensure credential/WebAuthn UI is suppressed *by policy* before navigation (not just by popup/WebRTC handlers). Add coverage/tests for the exact fallback path.
- Make security context unskippable in interfaces: if an IPC/API contract expands to include object-based security context (e.g., to select loopback transport vs public URL), update *all* call sites (including error/boot reauth flows) to use the canonical typed payload—never rely on string-only URLs in places where they can change routing semantics.

Example pattern (renderer + typed IPC):

```ts
// Renderer hardening: avoid a fallback that can show credential/WebAuthn UI.
try {
  window.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
  window.webContents.setWebRTCIPHandlingPolicy('disable_non_proxied_udp');

  // Ensure the session/policy for the title/hidden navigation suppresses
  // credential/WebAuthn UI before any navigation occurs.
  // (Apply/remove fallback paths so arbitrary public pages cannot slip in.)
} catch (e) {
  // Fail closed or log and abort navigation.
}
```

```ts
// IPC/auth: always pass the fully expressive payload to prevent bypass.
// Prefer object-based inputs so transport selection can’t be derived from a public URL string.
await ipcRenderer.invoke('probeConnectionConfig', {
  remoteUrl: config.remoteUrl,
  // include the fields needed for effective secure routing
  // (e.g., local_mtls_proxy / loopback transport metadata)
});
```

Result: security behavior stays consistent even during reauth/boot-failure handling and during unusual navigation/fallback scenarios.