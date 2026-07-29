---
title: Accessible React State Handling
description: In React components and hooks, changes to focus/interaction state or
  derived UI state must preserve correct behavior for all users and reflect the actual
  semantic state transitions.
repository: nousresearch/hermes-agent
label: React
language: TSX
comments_count: 2
repository_stars: 221948
---

In React components and hooks, changes to focus/interaction state or derived UI state must preserve correct behavior for all users and reflect the actual semantic state transitions.

Apply this standard:
1) Interactive controls: ARIA + roving focus requires keyboard support
- If you use a roving `tabIndex` (only the active tab is focusable), you must also implement expected keyboard navigation (typically ArrowLeft/ArrowRight/Home/End) to move focus/selection among tabs.
- Add tests that cover keyboard-only behavior (not just mouse).

Example (tablist pattern):
```tsx
function onTabKeyDown(e: React.KeyboardEvent, tabs: Tab[], currentId: string) {
  const idx = tabs.findIndex(t => t.id === currentId)
  const move = (nextIdx: number) => {
    const next = tabs[(nextIdx + tabs.length) % tabs.length]
    selectTab(next.id) // set active + update tabIndex
    focusTabButton(next.id) // optional: focus the newly selected tab button
  }

  switch (e.key) {
    case 'ArrowLeft': e.preventDefault(); move(idx - 1); break
    case 'ArrowRight': e.preventDefault(); move(idx + 1); break
    case 'Home': e.preventDefault(); move(0); break
    case 'End': e.preventDefault(); move(tabs.length - 1); break
  }
}
```

2) Hooks/effects: rerun on the semantic inputs, not just “session changes”
- Ensure `useEffect` dependency lists include the values that should trigger the behavior (e.g., language/locale).
- Avoid unnecessary resets by separating state that represents the “meaning” (e.g., placeholder kind/index selection) from state that only affects rendering (e.g., translated text).
- Add hook tests for:
  - changing language within an existing session
  - persistence transitions (null→id)
  - save/rollback behavior

Example (separate locale-independent selection from locale-dependent text):
```tsx
type PlaceholderSelection = { kind: 'new'|'followUp'; index: number }

function getPlaceholderText(sel: PlaceholderSelection, locale: string) {
  const templates = sel.kind === 'new' ? newTemplatesByLocale[locale] : followUpTemplatesByLocale[locale]
  return templates[sel.index]
}

// Keep sel stable; derive text from locale
const [sel, setSel] = useState<PlaceholderSelection>(() => ({ kind, index }))
const text = getPlaceholderText(sel, locale)
```

Net effect: keyboard-only users can operate interactive tab UI reliably, and hooks update derived text/state correctly when language or other semantic inputs change—without unintended rerolls or history resets.