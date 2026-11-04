---
title: "Library API diff"
code: "V1013.003"
slug: "library-api-diff"
technique: "API compatibility checking"
technique_id: "V1013"
technique_slug: "api-compatibility-checking"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Compare the exported symbols and signatures of a package against its last release."
repos: 0
craft:
  - "Run the public API comparison tool for the package's language against the last release tag."
  - "Fail the release job when the diff shows breaking changes and the version is not a major bump."
  - "Attach the API diff output to the release or the pull request."
reverse:
  - "A cargo semver-checks step in a release workflow or a japicmp plugin in a Maven or Gradle build."
  - "An api-extractor.json file or a griffe check step in CI."
packages:
  - id: "cargo-semver-checks"
    name: "cargo-semver-checks"
    url: "https://github.com/obi1kenobi/cargo-semver-checks"
  - id: "japicmp"
    name: "japicmp"
    url: "https://github.com/siom79/japicmp"
  - id: "api-extractor"
    name: "API Extractor (Rush Stack)"
    url: "https://github.com/microsoft/rushstack"
  - id: "griffe"
    name: "Griffe (griffe check)"
    url: "https://github.com/mkdocstrings/griffe"
tools: []
examples: []
---
