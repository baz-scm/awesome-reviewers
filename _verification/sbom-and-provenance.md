---
title: "SBOM and provenance"
id: "V1017"
slug: "sbom-and-provenance"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Records what went into a build and signs it, so consumers can verify where an artifact came from and what it contains."
subtechniques:
  - id: "V1017.001"
    name: "SBOM generation"
    description: "Emit an SPDX or CycloneDX bill of materials per release."
  - id: "V1017.002"
    name: "Signing and attestation"
    description: "Sign artifacts and attach build provenance (SLSA)."
packages:
  - id: "syft"
    name: "Syft"
    url: "https://github.com/anchore/syft"
  - id: "cosign"
    name: "Sigstore cosign"
    url: "https://github.com/sigstore/cosign"
  - id: "slsa-github-generator"
    name: "SLSA GitHub generator"
    url: "https://github.com/slsa-framework/slsa-github-generator"
craft:
  - "Generate an SBOM in the release workflow and publish it with the artifact."
  - "Sign with keyless signing from CI identity."
  - "Verify signatures in deployment."
reverse:
  - "Release workflows calling syft, cosign or actions/attest-build-provenance."
  - "*.sbom.json or *.intoto.jsonl assets on releases."
---
