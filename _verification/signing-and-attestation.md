---
title: "Signing and attestation"
code: "V1017.002"
slug: "signing-and-attestation"
technique: "SBOM and provenance"
technique_id: "V1017"
technique_slug: "sbom-and-provenance"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Sign artifacts and attach build provenance (SLSA)."
repos: 0
craft:
  - "Sign each release artifact in CI with keyless signing tied to the workflow identity."
  - "Generate SLSA build provenance for the artifact in the release workflow."
  - "Verify the signature and provenance before a deployment step runs."
reverse:
  - "A cosign sign or cosign sign-blob step in a release workflow."
  - "A *.intoto.jsonl provenance asset, or permissions: id-token: write on the release job."
packages:
  - id: "cosign"
    name: "Sigstore cosign"
    url: "https://github.com/sigstore/cosign"
  - id: "slsa-github-generator"
    name: "SLSA GitHub generator"
    url: "https://github.com/slsa-framework/slsa-github-generator"
tools: []
examples: []
---
