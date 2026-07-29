---
title: Explicit React UI Behavior
description: 'When building React components, make user interaction and lifecycle
  behavior explicit—particularly for accessibility and ref/state initialization.


  - Tooltips + disabled controls: If a disabled element can’t receive focus, put the
  focusable/hoverable semantics on a wrapper inside `TooltipTrigger asChild`, and
  use conditional `tabIndex` to avoid adding extra...'
repository: maximhq/bifrost
label: React
language: TSX
comments_count: 2
repository_stars: 6862
---

When building React components, make user interaction and lifecycle behavior explicit—particularly for accessibility and ref/state initialization.

- Tooltips + disabled controls: If a disabled element can’t receive focus, put the focusable/hoverable semantics on a wrapper inside `TooltipTrigger asChild`, and use conditional `tabIndex` to avoid adding extra tab stops. Don’t duplicate ARIA text that the tooltip system already wires up.

- Ref/state initialization: Prefer initializing refs/state directly from props (or a stable initializer) rather than using “ref-seeding” `useEffect` that can depend on effect ordering.

Example (tooltip focus + conditional tabIndex):
```tsx
<Tooltip>
  <TooltipTrigger asChild>
    <span tabIndex={!isEnabled ? 0 : undefined}>
      <button
        disabled={!isEnabled || isRefreshing}
        onClick={(e) => {
          e.stopPropagation();
          handleRefresh();
        }}
      >
        Refresh
      </button>
    </span>
  </TooltipTrigger>
  <TooltipContent>
    {isEnabled ? "Refresh list" : "Enable to refresh"}
  </TooltipContent>
</Tooltip>
```

Example (explicit ref init):
```tsx
const popupRef = useRef(initialPopup ?? null);
// Avoid useEffect(() => { popupRef.current = initialPopup ?? null }, [initialPopup])
```