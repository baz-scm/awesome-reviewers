---
title: Use descriptive names
description: Choose names that clearly indicate their purpose and behavior rather
  than using generic or ambiguous terms. Avoid internal abbreviations in user-facing
  content, ensure function names accurately reflect what they do, and prefer specific
  descriptive terms over generic ones.
repository: gravitational/teleport
label: Naming Conventions
language: Go
comments_count: 9
repository_stars: 19109
---

Choose names that clearly indicate their purpose and behavior rather than using generic or ambiguous terms. Avoid internal abbreviations in user-facing content, ensure function names accurately reflect what they do, and prefer specific descriptive terms over generic ones.

Examples of improvements:
- `handleWebsocketError` → `logWebsocketError` (function only logs, doesn't handle)
- `value bool` → `condition bool` (more specific parameter meaning)
- `mcp-access` → `mcp-user` (clarifies the actor/role purpose)
- `TeleportFlavor`/`TeleportPackage` → `TeleportArtifact`/`TeleportDirectory` (clearer distinction)
- `diagnostic.Diagnostic` → avoid repetitive package/type names
- `awsicPluginNameHelp` containing "AWSIC" → use full "AWS Identity Center integration"

This prevents confusion about functionality, makes code self-documenting, and improves maintainability by making the intent clear to future developers.