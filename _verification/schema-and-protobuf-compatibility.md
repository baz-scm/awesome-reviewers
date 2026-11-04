---
title: "Schema and protobuf compatibility"
code: "V1013.002"
slug: "schema-and-protobuf-compatibility"
technique: "API compatibility checking"
technique_id: "V1013"
technique_slug: "api-compatibility-checking"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Wire-compatibility rules for protobuf, Avro or JSON Schema."
repos: 0
craft:
  - "Add buf.yaml with a breaking section that selects the WIRE or WIRE_JSON category."
  - "Run buf breaking against the base branch of the protobuf module in CI."
  - "Block merges that fail buf breaking unless the pull request carries a breaking-change label."
reverse:
  - "A buf.yaml containing a breaking: block with use: categories."
  - "A buf breaking step in a CI workflow or a Makefile target."
packages:
  - id: "buf"
    name: "Buf (buf breaking)"
    url: "https://github.com/bufbuild/buf"
tools: []
examples: []
---
