---
title: End-to-end API Contract
description: 'When implementing or changing an API/host contract (REST headers, RPC
  operations, event payloads, or versioned endpoints), ensure the contract is honored
  end-to-end: what the caller sends/expects must be discoverable, correctly shaped,
  semantically consistent, and fully preserved through every conversion/projection.'
repository: cline/cline#v28
label: API
language: TypeScript
comments_count: 7
repository_stars: 70892
---

When implementing or changing an API/host contract (REST headers, RPC operations, event payloads, or versioned endpoints), ensure the contract is honored end-to-end: what the caller sends/expects must be discoverable, correctly shaped, semantically consistent, and fully preserved through every conversion/projection.

Apply these rules:
1) **Spec-compliant response shaping (no conditional spec gaps)**
   - If the spec says the host MUST NOT include something, don’t hide it only when a feature flag is set. Make the filtering unconditional based on the data.

2) **Payload/field invariants: “added fields must round-trip”**
   - When you add a request field or event property, thread it through *every* projection/copy: server → projector → runtime handler → forwarded event.
   - Add tests that assert both paths/payload copies include the field, including omitted/empty cases.

   Example pattern:
   ```ts
   // request -> event envelope
   envelope.displayPrompt = input.displayPrompt;

   // projector -> runtime conversion
   out.displayPrompt = in.displayPrompt;
   ```

3) **Semantic stability for headers and identifiers**
   - Don’t silently change what an existing header means.
   - If you must change the identifier, either keep the original meaning or rename/introduce a new header (e.g., `X-Task-ID` vs `X-Task-ULID`) and update backend routing accordingly.

4) **Discoverability/registration of RPC operations**
   - Ensure new operations are registered/exposed everywhere the client can reach them (e.g., Hub operation registries and compatibility layers). A missing registration is an API contract break.

5) **Endpoint versioning + normalization**
   - Verify the correct endpoint path/version (`/v1/...` vs `/v0/...`) and normalize base URLs (trailing slashes, optional prefixes) so clients hit the intended resource.

If you follow the above, you prevent the common failure modes demonstrated here: unreachable RPC ops, spec-violating response lists, “field goes in but never comes out,” silently reinterpreted headers, and incorrect versioned endpoint calls.