---
title: "SBOM and provenance"
code: "V1017"
slug: "sbom-and-provenance"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Records what went into a build and signs it, so consumers can verify where an artifact came from and what it contains."
subtechniques:
  - id: "V1017.001"
    name: "SBOM generation"
    slug: "sbom-generation"
    description: "Emit an SPDX or CycloneDX bill of materials per release."
  - id: "V1017.002"
    name: "Signing and attestation"
    slug: "signing-and-attestation"
    description: "Sign artifacts and attach build provenance (SLSA)."
---
