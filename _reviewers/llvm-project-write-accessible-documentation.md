---
title: Write accessible documentation
description: Documentation should be written with clarity and completeness to serve
  readers who may not have deep domain expertise. Use precise, unambiguous language
  that avoids technical jargon when simpler alternatives exist, and provide necessary
  context about origins, rationale, and background information.
repository: llvm/llvm-project
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 33702
---

Documentation should be written with clarity and completeness to serve readers who may not have deep domain expertise. Use precise, unambiguous language that avoids technical jargon when simpler alternatives exist, and provide necessary context about origins, rationale, and background information.

When writing technical documentation:
- Choose clear, direct phrasing over complex technical language
- Explain the "why" behind features, protocols, or implementations
- Include context about origins and relationships to other systems
- Consider how someone unfamiliar with the domain would interpret your words

Example of improvement:
Instead of: "This returns a hex-encoding list of 64-bit addresses for the frame PCs"
Write: "This returns a hex-encoded list of PC values, one for each frame of the call stack"

Additionally, include contextual notes such as: "Note: This packet is an LLDB extension to the GDB remote protocol, originated from [specific runtime/system]."