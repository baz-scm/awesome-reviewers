---
title: "Annotated screenshots"
code: "V1055.002"
slug: "annotated-screenshots"
technique: "Design conformance"
technique_id: "V1055"
technique_slug: "design-conformance"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Mark the differing regions so the fix is obvious."
repos: 0
craft:
  - "Load the screenshot and the design frame and find the regions that differ."
  - "Draw a box or outline around each differing region on the screenshot."
  - "Attach the annotated image to the pull request or the failing test."
reverse:
  - "A script that writes an annotated diff image as a CI artifact."
  - "Pillow or OpenCV in the test tooling dependencies."
packages:
  - id: "pillow"
    name: "Pillow"
    url: "https://github.com/python-pillow/Pillow"
  - id: "opencv"
    name: "OpenCV"
    url: "https://github.com/opencv/opencv"
tools: []
examples: []
---
