---
title: Respect provider context
description: 'Ensure library-provided integration points are used so styles and portals
  behave correctly in host environments (e.g., shadow roots, webcomponents).


  Motivation'
repository: likec4/likec4
label: React
language: TSX
comments_count: 2
repository_stars: 2582
---

Ensure library-provided integration points are used so styles and portals behave correctly in host environments (e.g., shadow roots, webcomponents).

Motivation
- Component libraries (Mantine, etc.) expose provider hooks/props for style nonces and portal targets. Using those prevents ad-hoc workarounds and avoids mismatched style injection or portals rendering outside the intended root.

How to apply
1) Use provider APIs for style nonces
- Prefer MantineProvider's getStyleNonce or the useMantineStyleNonce hook instead of manually passing nonce props around. Example pattern:

const root = document.getElementById('root') as HTMLDivElement
const nonce = root.getAttribute('nonce') || undefined

ReactDOM.createRoot(root).render(
  <MantineProvider theme={theme} getStyleNonce={() => nonce} forceColorScheme={scheme}>
    <LikeC4Context>
      <App />
    </LikeC4Context>
  </MantineProvider>
)

Or, if a component needs the nonce at runtime, use the hook inside the component:

function SomeComponent() {
  const styleNonce = useMantineStyleNonce()
  // use styleNonce when necessary
}

2) Forward portal/overlay props when rendering inside shadow roots
- If your component may render inside a shadow root or webcomponent, ensure overlay components (Tooltip, Popover, Modal, etc.) receive portal/target props so portals mount in the same root. Many libraries expose portalProps or accept a target prop. Example:

const ResetControlPointsButton = ({ portalProps }) => {
  return (
    <Tooltip label="Reset all control points" {...portalProps}>
      <Button>Reset</Button>
    </Tooltip>
  )
}

- When using a wrapper or custom button inside a host that provides portalProps, forward them to all overlay/portal-capable children.

Checklist
- Use provider hooks/props (getStyleNonce/useMantineStyleNonce) for style nonce management.
- Configure MantineProvider (or equivalent) at app root so all library components inherit the correct nonce/target.
- Forward portalProps to Tooltip/Popover/Modal/overlays when rendering inside webcomponents or shadow roots.
- Prefer library APIs over custom DOM hacks to keep behavior predictable and secure.

References: 0, 1