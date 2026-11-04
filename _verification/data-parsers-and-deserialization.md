---
title: "Data parsers and deserialization"
code: "V1059.003"
slug: "data-parsers-and-deserialization"
technique: "Attack surface inventory"
technique_id: "V1059"
technique_slug: "attack-surface-inventory"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "File, archive and object parsers that take untrusted input."
repos: 0
craft:
  - "List each parser for uploaded files, archives and serialized objects."
  - "Mark each parser as a component that takes untrusted input in the threat model."
  - "Record the size limits and parser libraries used for each input type."
reverse:
  - "A threat model entry for each file, archive or deserialization parser."
  - "Parser library versions pinned in the lockfile for the upload and deserialization code."
packages:
  - id: "pytm"
    name: "OWASP pytm"
    url: "https://github.com/OWASP/pytm"
  - id: "threagile"
    name: "Threagile"
    url: "https://github.com/Threagile/threagile"
  - id: "threat-dragon"
    name: "OWASP Threat Dragon"
    url: "https://github.com/OWASP/threat-dragon"
tools: []
examples: []
---
