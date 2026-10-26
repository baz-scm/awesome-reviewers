---
title: Design runtime-flexible APIs
description: When extending CRI/ABI-style APIs, avoid over-specifying runtime-variant
  behavior and instead make contracts that are both implementable and unambiguous
  for clients.
repository: kUbernetes/kUbernetes
label: API
language: Other
comments_count: 6
repository_stars: 128688
---

When extending CRI/ABI-style APIs, avoid over-specifying runtime-variant behavior and instead make contracts that are both implementable and unambiguous for clients.

Guidelines:
- Don’t hard-code format/media-type/validation constraints in the wire contract unless the ecosystem will enforce and conformance-test them. Prefer:
  - “Accepted formats determined by runtime” in the proto/API
  - Recommended formats/structure in KEP/docs.
- Define semantics for fields that change client behavior or observability (events/SLIs). For example, a “cached/present” boolean must precisely state what it means on success vs error.
  - If you use `cached`, explicitly document whether it applies to “no registry request made” and whether it is returned only on success.
- Model runtime capability support with explicit, granular capability fields (e.g., specific mount modes), not generic/version-dependent guesses.
  - This prevents kubelet/clients from assuming support for newly added options.
- For numeric/config fields:
  - Specify validation expectations (e.g., no duplicate keys; min/max bounds).
  - Choose primitive types and bounds to survive JSON/YAML round-tripping (avoid values beyond JS safe integer when using int-like fields).
  - Enforce constraints at the API layer where possible so invalid configs fail early, not after container/runtime attempts.

Example (semantic precision for cached):
```proto
// cached is true only when the profile is already present for this request and
// no registry/verification was performed. cached=false means the runtime
// actually checked/served/validated for this request (or the call failed).
// The field is only returned on successful calls.
bool cached = 1;
```