---
title: "SBOM generation"
code: "V1017.001"
slug: "sbom-generation"
technique: "SBOM and provenance"
technique_id: "V1017"
technique_slug: "sbom-and-provenance"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Emit an SPDX or CycloneDX bill of materials per release."
repos: 0
craft:
  - "Run syft against the release artifact or container image in the release workflow."
  - "Emit the bill of materials as SPDX or CycloneDX JSON."
  - "Upload the SBOM as a release asset next to the artifact."
reverse:
  - "A syft step in a release workflow or an anchore/sbom-action usage."
  - "*.sbom.json or *.spdx.json files attached to releases."
packages:
  - id: "syft"
    name: "Syft"
    url: "https://github.com/anchore/syft"
tools: []
examples: []
---
