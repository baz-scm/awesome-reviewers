---
title: Gate UI features
description: Ensure UI elements (buttons, icons, tooltips, overlays) are only registered
  or rendered when the corresponding configuration or feature flag is enabled. Also
  ensure feature flags are passed into components or a central store so components
  make rendering decisions from configuration rather than hard-coded assumptions.
repository: likec4/likec4
label: Configurations
language: TSX
comments_count: 2
repository_stars: 2582
---

Ensure UI elements (buttons, icons, tooltips, overlays) are only registered or rendered when the corresponding configuration or feature flag is enabled. Also ensure feature flags are passed into components or a central store so components make rendering decisions from configuration rather than hard-coded assumptions.

Motivation
- Prevents exposing unavailable features, avoids UI clutter, and keeps behavior predictable across environments.
- Matches existing patterns where flags are passed from top-level props into stores/components.

How to apply
1. Propagate flags: accept feature flags as props at top-level components and pass them into your UI components or into the app/store.
   Example pattern (top-level):
   // LikeC4Diagram.tsx (pattern reference)
   <LikeC4Diagram enableSearch={enableSearch} />

2. Gate registration: only add buttons/actions to arrays when the flag is true.
   Example:
   const buttons = []
   if (flags.enableVscode) {
     buttons.push({
       id: 'open-in-vscode',
       label: 'Open in VSCode',
       onClick: () => { /* ... */ },
     })
   }

3. Gate rendering: only render optional UI elements in JSX when the flag is true or derived from the store/props.
   Example:
   <ActionIconGroup>
     {flags.enableSearch && (
       <Tooltip label="Search">
         <ActionIcon>/* icon */</ActionIcon>
       </Tooltip>
     )}
   </ActionIconGroup>

Notes
- Prefer a single source of truth for flags (props -> context/store) to avoid mismatches.
- Keep gating logic simple and colocated with the registration or render site so it's obvious why an element may be absent.
- Include tests or story variants for both enabled and disabled states to prevent regressions.