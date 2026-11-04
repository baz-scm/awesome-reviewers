---
title: "Design conformance"
id: "V1055"
slug: "design-conformance"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Compares the rendered UI with the design it implements and reports layout, spacing, colour and copy differences."
subtechniques:
  - id: "V1055.001"
    name: "Design-to-render comparison"
    description: "Diff a screenshot against the exported design frame."
  - id: "V1055.002"
    name: "Annotated screenshots"
    description: "Mark the differing regions so the fix is obvious."
packages:
  - id: "pixelmatch"
    name: "pixelmatch"
    url: "https://github.com/mapbox/pixelmatch"
  - id: "opencv"
    name: "OpenCV"
    url: "https://github.com/opencv/opencv"
  - id: "pillow"
    name: "Pillow"
    url: "https://github.com/python-pillow/Pillow"
  - id: "playwright"
    name: "Playwright"
    url: "https://github.com/microsoft/playwright"
craft:
  - "Export frames at the same viewport the test renders."
  - "Compare with a tolerance and mask dynamic content."
  - "Annotate differing regions on the screenshot."
reverse:
  - "Design links in tickets or PRs, and exported frames in the repository."
---
