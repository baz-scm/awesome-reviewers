---
title: Deterministic Security Profile Semantics
description: When defining security-policy APIs (e.g., seccomp/AppArmor profiles),
  make the effective policy computation and schema evolution unambiguous and compatibility-safe.
repository: kUbernetes/kUbernetes
label: Security
language: Other
comments_count: 2
repository_stars: 128688
---

When defining security-policy APIs (e.g., seccomp/AppArmor profiles), make the effective policy computation and schema evolution unambiguous and compatibility-safe.

- **Specify exact composition rules**: If multiple profile sources can apply (runtime baseline + optional base + OCI digest-pinned profile), document and implement a single deterministic computation path. Avoid vague “merge” behavior.
  - Example rule to follow:
    ```text
    effective_profile = intersect(
      (base_profile ? base_profile : runtime_default_or_localhost_replacement),
      oci_ref_digest_pinned_profile
    )
    ```
  - If a “local/localhost base” is intended to override the runtime default, codify that as a **replacement**, not an additional merge.

- **Conservatively evolve security mechanism types**: Only add new `kind` values (e.g., AppArmor) when runtimes can safely parse and enforce them.
  - Ensure **unknown/unsupported kinds are rejected** (do not “accept and ignore”), so security behavior doesn’t silently degrade.

- **Keep type applicability clear**: If a field applies only to one profile type (e.g., `oci_ref` only when `ProfileType` is `OCI`), require runtimes to **ignore it otherwise**; this prevents unintended cross-type policy application.

These practices reduce the risk of insecure defaults, policy ambiguity, and accidental enforcement gaps during API evolution.